"""
Schema definitions for the silver layer where data is cleaned and normalised.
"""

from ..metadata import metadata
from ..sql import (
    Array,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    String,
    Table,
    Uuid,
)

link = Table(
    "link",
    metadata,
    Column("source_id", Uuid(as_uuid=True)),
    Column("source_entity", Uuid(as_uuid=True)),
    Column("target_id", Uuid(as_uuid=True)),
    Column("target_entity", String),
    Column("relation_type", String),
    schema="silver",
)

person = Table(
    "person",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("given_name", String),
    Column("family_name", String),
    Column("orcid_id", String),
    schema="silver",
)

person_link = Table(
    "person_link",
    metadata,
    Column("source_id", Uuid(as_uuid=True)),
    Column("target_entity", String),
    Column("target_id", Uuid(as_uuid=True)),
    Column("href", String),
    Column("relation_type", String),
    schema="silver",
)

organisation = Table(
    "organisation",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("name", String),
    schema="silver",
)

organisation_link = Table(
    "organisation_link",
    metadata,
    Column("source_id", Uuid(as_uuid=True)),
    Column("target_entity", String),
    Column("target_id", Uuid(as_uuid=True)),
    Column("href", String),
    Column("relation_type", String),
    schema="silver",
)


organisation_address = Table(
    "organisation_address",
    metadata,
    Column("organisation_id", Uuid(as_uuid=True)),
    Column("id", Uuid(as_uuid=True)),
    Column("line1", String),
    Column("line2", String),
    Column("line3", String),
    Column("line4", String),
    Column("line5", String),
    Column("city", String),
    Column("county", String),
    Column("post_code", String),
    Column("region", String),
    Column("country", String),
    Column("type", String),
    schema="silver",
)

fund = Table(
    "fund",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("start_date", DateTime),
    Column("end_date", DateTime),
    Column("amount", BigInteger),
    Column("currency_code", String),
    Column("category", String),
    schema="silver",
    # catalog="silver",
)

project = Table(
    "project",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("title", String),
    Column("status", String),
    Column("grant_category", String),
    Column("lead_funder", String),
    Column("lead_department", String),
    Column("abstract", String),
    Column("tech_abstract", String),
    Column("potential_impact", String),
    Column("start_date", DateTime),
    Column("end_date", DateTime),
    schema="silver",
)

# TODO:
# project_identifier (raw_data->'identifiers'->'identifier')
# project_category ‣ select raw_data->>'id' id, raw_data->'healthCategories'->'healthCategory' health_cat, json_keys(raw_data) from raw limit 10;
# project_activity (raw_data->'researchActivities'->'researchActivity')
# project_subject (raw_data->'researchSubjects'->'researchSubject')
# project_topic (raw_data->'researchTopics'->'researchTopic')
# project_programme (raw_data->'rcukProgrammes'->'rcukProgramme')
# project_participant (raw_data->'participantValues'->'participant')


### Outcomes ###

collaboration = Table(
    "collaboration",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),  # All seem to be null
    Column("description", String),
    Column("parent_organisation", String),
    Column("child_organisation", String),
    Column("principal_investigator_contribution", String),
    Column("partner_contribution", String),
    Column("start_date", DateTime),
    Column("end_date", DateTime),  # All seem to be null
    Column("sector", String),
    Column("country", String),
    Column("impact", String),
    Column("supporting_url", String),
    schema="silver",
)


artistic_and_creative_product = Table(
    "artistic_and_creative_product",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),
    Column("description", String),
    Column("type", String),
    Column("impact", String),
    Column("year_first_provided", String),
    Column("supporting_url", String),
    schema="silver",
)

dissemination = Table(
    "dissemination",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),  # All seem to be null
    Column("description", String),
    Column("form", String),
    Column("primary_audience", String),
    Column("years_of_dissemination", Array(String)),
    # Column("results", String),  # All seem to be null
    Column("impact", String),
    Column("presentation_type", String),
    Column("geographic_reach", String),
    Column("part_of_official_scheme", Boolean),
    Column("supporting_url", String),
    schema="silver",
)

further_funding = Table(
    "further_funding",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),  # All seem to be null
    Column("description", String),
    # Column("narrative", String), # All seem to be null
    Column("amount", BigInteger),
    Column("currency_code", String),
    Column("organisation", String),
    Column("department", String),
    Column("funding_id", String),
    Column("start_date", DateTime),
    Column("end_date", DateTime),
    Column("sector", String),
    Column("country", String),
    schema="silver",
)

impact_summary = Table(
    "impact_summary",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),  # All seem to be null
    Column("description", String),
    Column("impact_types", Array(String)),
    # Column("summary", String), # All seem to be null
    # Column("beneficiaries", String), # All seem to be null
    # Column("contribution_method", String), # All seem to be null
    Column("sector", String),
    Column("first_year_of_impact", String),
    schema="silver",
)

intellectual_property = Table(
    "intellectual_property",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),  # All seem to be null
    Column("description", String),
    Column("protection", String),
    Column("patent_id", String),
    Column("year_protection_granted", String),
    # Column("type", String),  # All seem to be null
    Column("impact", String),
    Column("licensed", String),
    # Column("patent_url", String),  # All seem to be null
    # Column("start_date", DateTime), # All seem to be null
    # Column("end_date", DateTime), # All seem to be null
    schema="silver",
)

key_finding = Table(
    "key_finding",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("description", String),
    # Column("non_academic_uses", String), # All seem to be null
    Column("exploitation_pathways", String),
    Column("sectors", Array(String)),
    Column("supporting_url", String),
    schema="silver",
)

policy_influence = Table(
    "policy_influence",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("influence", String),
    Column("type", String),
    Column("guideline_title", String),
    Column("impact", String),
    # Column("methods", String), # All seem to be null
    # Column("areas", Array(String)), # All seem to be null
    Column("geographic_reach", String),
    Column("supporting_url", String),
    schema="silver",
)

product = Table(
    "product",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),
    Column("description", String),
    Column("type", String),
    Column("stage", String),
    Column("clinical_trial", String),
    Column("ukcrn_isctn_id", String),
    Column("year_development_completed", String),
    Column("impact", String),
    Column("supporting_url", String),
    schema="silver",
)


research_database_and_model = Table(
    "research_database_and_model",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),
    Column("description", String),
    Column("type", String),
    Column("impact", String),
    Column("provided_to_others", Boolean),
    Column("year_first_provided", String),
    Column("supporting_url", String),
    schema="silver",
)

research_material = Table(
    "research_material",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),
    Column("description", String),
    Column("type", String),
    Column("impact", String),
    # Column("software_developed", String), # All seem to be null
    # Column("software_open_sourced", String), # All seem to be null
    Column("provided_to_others", Boolean),
    Column("year_first_provided", String),
    Column("supporting_url", String),
    schema="silver",
)

software_and_technical_product = Table(
    "software_and_technical_product",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),
    Column("description", String),
    Column("type", String),
    Column("impact", String),
    Column("software_open_sourced", Boolean),
    # Column("open_source_license", String),  # All seem to be null
    Column("year_first_provided", String),
    Column("supporting_url", String),
    schema="silver",
)

spinout = Table(
    "spinout",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("description", String),
    Column("company_name", String),
    # Column("company_description", String), # All seem to be null
    Column("impact", String),
    Column("website", String),
    Column("registration_number", String),  # All seem to be null
    Column("year_established", String),
    # Column("ip_exploited", String), # All seem to be null
    # Column("joint_venture", String), # All seem to be null
    schema="silver",
)


publication = Table(
    "publication",
    metadata,
    Column("id", Uuid(as_uuid=True)),
    Column("outcome_id", String),
    Column("title", String),
    Column("type", String),
    # Column("abstract", String), # All seem to be null
    # Column("other_information", String), # All seem to be null
    Column("journal_title", String),
    Column("date_published", DateTime),
    Column("publication_url", String),
    Column("pub_med_id", String),
    Column("isbn", String),
    Column("issn", String),
    # Column("series_number", String), # All seem to be null
    # Column("series_title", String), # All seem to be null
    # Column("sub_title", String), # All seem to be null
    Column("volume_title", String),
    Column("doi", String),
    # Column("volume_number", String), # All seem to be null
    Column("issue", String),
    # Column("total_pages", String), # All seem to be null
    Column("edition", String),
    # Column("chapter_number", String), # All seem to be null
    Column("chapter_title", String),
    Column("page_reference", String),
    # Column("conference_event", String), # All seem to be null
    # Column("conference_location", String), # All seem to be null
    # Column("conference_number", String), # All seem to be null
    Column("author", String),
    schema="silver",
)
