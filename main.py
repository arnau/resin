import duckdb

from resin.fetcher import fetch_all_entities, setup_database


def main():
    conn = duckdb.connect("resin_landing.duckdb")
    setup_database(conn)
    fetch_all_entities(conn)

    # 6 projects linked by fund
    # EP/Z531200/1


if __name__ == "__main__":
    main()
