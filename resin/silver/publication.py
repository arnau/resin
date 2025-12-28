"""
Publication (outcome) transformation queries for the silver layer.
"""

from resin.bronze import schema as bronze
from resin.silver.schema import publication
from resin.sql import (
    Uuid,
    pick,
    pick_as,
    pick_as_ts,
    select,
    unnest,
)


def _raw():
    """Extract raw data from bronze layer."""
    return (
        select(unnest(bronze.api_page.c.raw_data).label("raw_data"))
        .where(bronze.api_page.c.entity == "publication")
        .cte("raw")
    )


def _fieldset():
    """Transform raw data into final format."""
    raw = _raw()
    raw_data = raw.c.raw_data

    return (
        select(
            pick_as(raw_data, "$.id", Uuid).label("id"),
            pick(raw_data, "$.outcomeid").label("outcome_id"),
            pick(raw_data, "$.title").label("title"),
            pick(raw_data, "$.type").label("type"),
            # pick(raw_data, "$.abstractText").label("abstract"),
            # pick(raw_data, "$.otherInformation").label("other_information"),
            pick(raw_data, "$.journalTitle").label("journal_title"),
            pick_as_ts(raw_data, "$.datePublished").label("date_published"),
            pick(raw_data, "$.publicationUrl").label("publication_url"),
            pick(raw_data, "$.pubMedId").label("pub_med_id"),
            pick(raw_data, "$.isbn").label("isbn"),
            pick(raw_data, "$.issn").label("issn"),
            # pick(raw_data, "$.seriesNumber").label("series_number"),
            # pick(raw_data, "$.seriesTitle").label("series_title"),
            # pick(raw_data, "$.subTitle").label("sub_title"),
            pick(raw_data, "$.volumeTitle").label("volume_title"),
            pick(raw_data, "$.doi").label("doi"),
            # pick(raw_data, "$.volumeNumber").label("volume_number"),
            pick(raw_data, "$.issue").label("issue"),
            # pick(raw_data, "$.totalPages").label("total_pages"),
            pick(raw_data, "$.edition").label("edition"),
            # pick(raw_data, "$.chapterNumber").label("chapter_number"),
            pick(raw_data, "$.chapterTitle").label("chapter_title"),
            pick(raw_data, "$.pageReference").label("page_reference"),
            # pick(raw_data, "$.conferenceEvent").label("conference_event"),
            # pick(raw_data, "$.conferenceLocation").label("conference_location"),
            # pick(raw_data, "$.conferenceNumber").label("conference_number"),
            pick(raw_data, "$.author").label("author"),
        )
        .select_from(raw)
        .cte("fieldset")
    )


def select_all():
    return select("*").select_from(_fieldset())


def insert_all():
    """Insert statement for dissemination table."""
    return publication.insert().from_select(list(publication.columns), _fieldset())
