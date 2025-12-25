from sqlalchemy import JSON, UUID, func, select
from sqlalchemy.dialects import postgresql as pg

from .organisation import organisation_raw
from .schema import organisation_address


def address_raw():
    organisation_raw_cte = organisation_raw()

    return (
        select(
            func.cast(
                func.json_extract_string(organisation_raw_cte.c.raw_data, "$.id"), UUID
            ).label("organisation_id"),
            func.unnest(
                func.cast(
                    func.json_extract(
                        organisation_raw_cte.c.raw_data, "$.addresses.address"
                    ),
                    pg.ARRAY(JSON),
                )
            ).label("address"),
        )
        .select_from(organisation_raw_cte)
        .cte("address_raw")
    )


def address():
    address_raw_cte = address_raw()

    return (
        select(
            address_raw_cte.c.organisation_id,
            func.cast(
                func.json_extract_string(address_raw_cte.c.address, "$.id"), UUID
            ).label("id"),
            func.json_extract_string(address_raw_cte.c.address, "$.line2").label(
                "line2"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.line1").label(
                "line1"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.line3").label(
                "line3"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.line4").label(
                "line4"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.line5").label(
                "line5"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.city").label("city"),
            func.json_extract_string(address_raw_cte.c.address, "$.county").label(
                "county"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.postCode").label(
                "post_code"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.region").label(
                "region"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.country").label(
                "country"
            ),
            func.json_extract_string(address_raw_cte.c.address, "$.type").label("type"),
        )
        .select_from(address_raw_cte)
        .cte("address")
    )


def organisation_address_select():
    return select("*").select_from(address())


def organisation_address_insert():
    return organisation_address.insert().from_select(
        list(organisation_address.columns), organisation_address_select()
    )
