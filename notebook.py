# %% prelude
import json

import duckdb
import sqlparse
from sqlalchemy import (
    DDL,
    JSON,
    UUID,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    column,
    func,
    literal,
    literal_column,
    text,
)
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement, select
from sqlalchemy.sql.expression import Executable


class CreateTableAs(Executable, ClauseElement):
    inherit_cache = False

    def __init__(self, name, query):
        self.name = name
        self.query = query


@compiles(CreateTableAs)
def visit_create_table_as(element, compiler, **kw):
    return "CREATE TABLE %s AS %s" % (
        element.name,
        compiler.process(element.query, **kw),
    )


conn = duckdb.connect(":memory:")
conn.execute("""
    attach 'resin_landing.duckdb' as landing (READ_ONLY);
    attach 'resin_workshop.duckdb' as workshop (READ_ONLY);
    use workshop;
""")


def print_sql(stmt: ClauseElement):
    d = pg.dialect()
    q = stmt.compile(dialect=d, compile_kwargs={"literal_binds": True})
    print(sqlparse.format(str(q), reindent_aligned=True))


# %% query
res = conn.execute("""
    WITH person_blob AS (
        SELECT
            unnest(person) AS person
        FROM
            landing.person_raw
    ),
    person_schema AS (
        SELECT
            json_structure(person) AS schema
        FROM
            person_blob
    )
    select
        schema
    from
        person_schema
    limit 1
""").fetchone()


schema = json.loads(res[0])
sch = {
    "links": {
        "link": [
            {
                "href": "VARCHAR",
                "rel": "VARCHAR",
                "start": "UBIGINT",
                "end": "UBIGINT",
                "otherAttributes": "JSON",
            }
        ]
    },
    "ext": "VARCHAR",
    "id": "UUID",
    "outcomeid": "VARCHAR",
    "href": "VARCHAR",
    "created": "UBIGINT",
    "updated": "UBIGINT",
    "firstName": "VARCHAR",
    "otherNames": "VARCHAR",
    "surname": "VARCHAR",
    "email": "VARCHAR",
    "orcidId": "VARCHAR",
}

# %% parse json
res = conn.execute(f"""
    WITH person_blob AS (
        SELECT
            unnest(person) AS person
        FROM
            person_raw
    ),
    person AS (
        SELECT
            from_json(person, '{json.dumps(sch)}') AS person
        FROM
            person_blob
    )
    select
        person.links
    from
        person
    limit 1
""").fetchone()


# Iterate over the 'link' key
if res[0] and "link" in res[0]:
    for link in res[0]["link"]:
        print("Link item:")
        for link_key, link_value in link.items():
            print(f"  {link_key}: {link_value}")

# %% workshop.person_raw

# %% workshop.person_link
#
# create table person_link as select id, unnest(links.link, recursive := true) from (select cast(person->>'id' as uuid) as id, from_json(person->'links', '{"link": [{"href": "varchar", "rel":"varchar", "start":"ubigint", "end":"ubigint","otherAttributes":"json"}]}') links from (select unnest(person) person from landing.person_raw));

# %% SQLAlchemy Core equivalent

metadata = MetaData()
landing_person = Table("person_raw", metadata, Column("person", JSON), schema="landing")

person_raw = select(
    func.unnest(landing_person.c.person).label("person"),
).cte("person_raw")

person_link_schema = """[{"href":"VARCHAR","rel":"VARCHAR","start":"UBIGINT","end":"UBIGINT","otherAttributes":"JSON"}]"""
person_parsed = (
    select(
        func.cast(text("person->>'id'"), UUID).label("id"),
        # func.cast(person_raw.c.person["id"], UUID).label("id2"),
        func.from_json(
            text("person->'links'->'link'"), literal(person_link_schema)
        ).label("links"),
    )
    .select_from(person_raw)
    .cte("person_parsed")
)

person_link_query = (
    select(
        person_parsed.c.id,
        func.unnest(person_parsed.c.links, text("recursive:=True")).label("link"),
    )
    .select_from(person_parsed)
    .cte(
        "person_link",
    )
)

person_link = (
    select(
        person_link_query.c.id.label("source_id"),
        func.array_extract(func.parse_path(text("href")), -2).label("target_entity"),
        func.array_extract(func.parse_path(text("href")), -1).label("target_id"),
        literal_column("rel").label("relation_type"),
        literal_column("href").label("url"),
    )
    .select_from(person_link_query)
    .where(literal_column("rel") != "ORCID_ID")
)

table_person_link = CreateTableAs("person_link", person_link)

print_sql(table_person_link)
