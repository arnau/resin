from resin.sql import (
    JsonArray,
    Uuid,
    pick,
    pick_as,
    select,
    unnest,
)

from . import organisation
from .schema import organisation_address


def _raw():
    raw = organisation._raw()  # type: ignore

    return (
        select(
            pick_as(raw.c.raw_data, "$.id", Uuid).label("organisation_id"),
            unnest(
                pick_as(raw.c.raw_data, "$.addresses.address", JsonArray),
            ).label("address"),
        )
        .select_from(raw)
        .cte("address_raw")
    )


def _fieldset():
    raw = _raw()

    return (
        select(
            raw.c.organisation_id,
            pick_as(raw.c.address, "$.id", Uuid).label("id"),
            pick(raw.c.address, "$.line2").label("line2"),
            pick(raw.c.address, "$.line1").label("line1"),
            pick(raw.c.address, "$.line3").label("line3"),
            pick(raw.c.address, "$.line4").label("line4"),
            pick(raw.c.address, "$.line5").label("line5"),
            pick(raw.c.address, "$.city").label("city"),
            pick(raw.c.address, "$.county").label("county"),
            pick(raw.c.address, "$.postCode").label("post_code"),
            pick(raw.c.address, "$.region").label("region"),
            pick(raw.c.address, "$.country").label("country"),
            pick(raw.c.address, "$.type").label("type"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select("*").select_from(_fieldset())


def insert_all():
    return organisation_address.insert().from_select(
        list(organisation_address.columns), _fieldset()
    )
