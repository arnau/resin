import time
from urllib.parse import urlencode, urlunparse

import duckdb

entity_mapping = {
    "fund": "funds",
    "project": "projects",
    "person": "persons",
    "organisation": "organisations",
    "artisticandcreativeproduct": "outcomes/artisticandcreativeproducts",
    "collaboration": "outcomes/collaborations",
    "dissemination": "outcomes/disseminations",
    # "exploitation": "outcomes/exploitations",
    # WARN: the response is missing an R so we use "futherfunding" rather than "furtherfunding"
    "futherfunding": "outcomes/furtherfundings",
    "impactsummary": "outcomes/impactsummaries",
    "intellectualproperty": "outcomes/intellectualproperties",
    "keyfinding": "outcomes/keyfindings",
    "policyinfluence": "outcomes/policyinfluences",
    "product": "outcomes/products",
    "researchdatabaseandmodel": "outcomes/researchdatabaseandmodels",
    "researchmaterial": "outcomes/researchmaterials",
    "softwareandtechnicalproduct": "outcomes/softwareandtechnicalproducts",
    "spinout": "outcomes/spinouts",
    # "otherresearchitem": "outcomes/otherresearchitems",
    "publication": "outcomes/publications",
}


def make_url(entity: str, page: int, size: int = 100):
    """
    Helper function to compose URLs for the GTR API.
    """

    return urlunparse(
        (
            "https",
            "gtr.ukri.org",
            f"/gtr/api/{entity_mapping[entity]}",
            "",
            urlencode({"p": page, "s": size}),
            "",
        )
    )


def fetch(conn: duckdb.DuckDBPyConnection, entity: str, page: int):
    table_name = f"{entity}_raw"
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            links json[],
            ext json,
            page int64,
            size int64,
            totalPages int64,
            totalSize int64,
            {entity} json[]
        );
    """)

    while True:
        current_url = make_url(entity, page)
        query = f"""
            BEGIN TRANSACTION;
            INSERT INTO {table_name} from read_json('{current_url}');

            INSERT INTO tracker (entity, page, status) VALUES ('{entity}', {page}, 'incomplete')
            ON CONFLICT DO UPDATE set page = {page};

            COMMIT;
        """

        try:
            conn.execute(query).fetchall()
            print(f"{entity}: Page {page}")
            page += 1
            time.sleep(0.8)
        except Exception as e:
            # An explicit rollback is needed before attempting to update
            # on 404.
            try:
                conn.execute("ROLLBACK;")
            except Exception as _e:
                pass

            if "404" in str(e):
                conn.execute(
                    "UPDATE tracker SET status = 'complete' WHERE entity = ?", (entity,)
                )
                print(f"Reached end at page {page}")
                break
            elif "429" in str(e):
                print("Rate limit exceeded. Waiting for 5 minutes")
                time.sleep(300)
            else:
                raise e


def main():
    conn = duckdb.connect("resin_landing.duckdb")
    conn.execute("""
        CREATE SECRET http (
            TYPE http,
            EXTRA_HTTP_HEADERS map {
                'Accept': 'application/json'
            }
        );
        CREATE TABLE IF NOT EXISTS tracker (
            entity varchar PRIMARY KEY,
            page int,
            status varchar,
            timestamp TIMESTAMP DEFAULT current_timestamp
        );
    """)

    sorted_entities = sorted(entity_mapping.keys())
    for entity in sorted_entities:
        res = conn.execute(
            "SELECT page, status FROM tracker WHERE entity = ?", (entity,)
        ).fetchall()
        if len(res) == 0:
            fetch(conn, entity, 1)
        else:
            page, status = res[0]
            if status == "incomplete":
                fetch(conn, entity, page + 1)
            elif status == "complete":
                print(f"No more work for {entity}.")
            else:
                print(f"Skipping {entity} due to unknown status")

    # 6 projects linked by fund
    # EP/Z531200/1


if __name__ == "__main__":
    main()
