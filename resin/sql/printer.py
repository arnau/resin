from enum import Enum
from typing import Any, Dict, Optional

import sqlparse
from sqlalchemy import ClauseElement, Compiled
from sqlalchemy.dialects import postgresql as pg
from sqlfmt.api import Mode, format_string


class SqlFormatter(Enum):
    SqlParse = "sqlparse"
    SqlFmt = "sqlfmt"
    Nil = "nil"


def format_sql(stmt: ClauseElement, options: Optional[Dict[str, Any]] = None) -> str:
    if options is None:
        options = {}

    formatter: SqlFormatter = options.get("formatter", SqlFormatter.SqlParse)
    dialect = pg.dialect()
    query = stmt.compile(dialect=dialect, compile_kwargs={"literal_binds": True})

    match formatter:
        case SqlFormatter.SqlParse:
            res = fmt_sqlparse(query)
        case SqlFormatter.SqlFmt:
            res = fmt_sqlfmt(query)
        case _:
            res = query

    return str(res)


def print_sql(stmt: ClauseElement, options: Optional[Dict[str, Any]] = None) -> None:
    print(format_sql(stmt, options))


def fmt_sqlparse(query: Compiled) -> str:
    return sqlparse.format(str(query), reindent_aligned=True, column_align=True)


def fmt_sqlfmt(query: Compiled) -> str:
    mode = Mode()

    return format_string(str(query), mode)
