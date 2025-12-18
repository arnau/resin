import time
from datetime import datetime
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


def get_total_pages(conn: duckdb.DuckDBPyConnection, table_name: str):
    total_pages_result = conn.execute(
        f"SELECT totalPages FROM {table_name} LIMIT 1;"
    ).fetchone()
    return total_pages_result[0] if total_pages_result else None


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

    total_pages = get_total_pages(conn, table_name)

    while True:
        current_url = make_url(entity, page)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if total_pages is not None and page > total_pages:
            # We reached the last page.
            conn.execute(
                """
                UPDATE tracker
                SET status = 'complete', timestamp = ?
                WHERE entity = ?
                """,
                (timestamp, entity),
            )
            break

        try:
            conn.execute(f"""
                BEGIN TRANSACTION;

                INSERT INTO {table_name} from read_json('{current_url}');
                INSERT INTO tracker
                    (entity, page, status, timestamp)
                VALUES
                    ('{entity}', {page}, 'incomplete', '{timestamp}')
                ON CONFLICT DO UPDATE
                    set page = {page};

                COMMIT;
            """).fetchall()

            # Update cache after first successful insert
            if total_pages is None:
                total_pages = get_total_pages(conn, table_name)

            print(f"{timestamp} - {entity}: Page {page}/{total_pages}")
            page += 1
            time.sleep(0.8)
        except Exception as e:
            # An explicit rollback is needed before attempting to retry.
            try:
                conn.execute("ROLLBACK;")
            except Exception as _e:
                pass

            if "429" in str(e):
                print("Rate limit exceeded. Waiting for 5 minutes")
                time.sleep(300)
            if "503" in str(e):
                print("Service unavailable. Waiting for 5 minutes")
                time.sleep(300)
            else:
                raise e


def setup_database(conn: duckdb.DuckDBPyConnection):
    """Initialize the database with necessary tables and configurations."""
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


def fetch_all_entities(conn: duckdb.DuckDBPyConnection):
    """Fetch data for all entities, continuing from where we left off."""
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
