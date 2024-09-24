from datetime import datetime
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, ConfigDict, Field


FIELD_NAMES_TO_BE_CAPITALIZED = ['url', 'doi', 'issn', 'isbn', 'orcid']


class DoiBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda name: name.upper() if name in FIELD_NAMES_TO_BE_CAPITALIZED else name.replace('_', '-'),
        extra='forbid'
    )


class DoiDateTime(DoiBaseModel):
    date_parts: Annotated[list[list[int] | list[None]], Len(min_length=1)]
    date_time: datetime | None = None
    timestamp: int | None = None


class DoiLicense(DoiBaseModel):
    start: DoiDateTime
    content_version: str
    delay_in_days: int
    url: str


class DoiContentDomain(DoiBaseModel):
    domain: list[str]
    crossmark_restriction: bool


class DoiAffiliation(DoiBaseModel):
    name: str


class DoiAuthor(DoiBaseModel):
    name: str | None = None
    family: str | None = None
    given: str | None = None
    affiliation: list[DoiAffiliation] | None = None
    sequence: str | None = None
    authenticated_orcid: bool | None = None
    orcid: str | None = None


class DoiReference(DoiBaseModel):
    key: str

    article_title: str | None = None
    journal_title: str | None = None
    volume_title: str | None = None
    series_title: str | None = None

    # These seem different compared to the same fields in DoiData
    isbn_type: str | None = None
    isbn: str | None = None

    issn_type: str | None = None
    issn: str | None = None

    content_domain: DoiContentDomain | None = None
    doi_asserted_by: str | None = None
    unstructured: str | None = None
    first_page: str | None = None
    edition: str | None = None
    volume: str | None = None
    author: str | None = None
    issue: str | None = None
    year: str | None = None
    doi: str | None = None


class DoiLink(DoiBaseModel):
    url: str
    content_type: str
    content_version: str
    intended_application: str


class DoiResourceLink(DoiBaseModel):
    url: str


class DoiResource(DoiBaseModel):
    primary: DoiResourceLink


class DoiJournalIssue(DoiBaseModel):
    issue: str
    published_print: DoiDateTime | None = None
    published_online: DoiDateTime | None = None


class DoiAssertionGroup(DoiBaseModel):
    name: str
    label: str


class DoiAssertion(DoiBaseModel):
    value: str
    name: str
    label: str
    order: int | None = None
    url: str | None = None
    group: DoiAssertionGroup | None = None


class DoiRelation(DoiBaseModel):
    pass


class DoiSubject(DoiBaseModel):
    pass


class DoiIsbn(DoiBaseModel):
    type: str
    value: str


class DoiFunderId(DoiBaseModel):
    id: str
    id_type: str
    asserted_by: str


class DoiFunder(DoiBaseModel):
    name: str
    doi: str | None = None
    doi_asserted_by: str | None = None

    award: Annotated[list[str], Field(default_factory=list)]
    id: Annotated[list[DoiFunderId], Field(default_factory=list)]


class DoiStandardsBody(DoiBaseModel):
    name: str
    acronym: str


class DoiUpdatedBy(DoiBaseModel):
    updated: DoiDateTime
    doi: str
    type: str
    label: str


class DoiData(DoiBaseModel):
    publisher: str
    title: str
    type: str
    doi: str
    url: str

    resource: DoiResource | None = None
    relation: DoiRelation | None =None
    subject: list[DoiSubject] | None = None

    is_referenced_by_count: int | None = None
    references_count: int | None = None
    reference_count: int | None = None
    score: int | None = None

    issued: DoiDateTime
    deposited: DoiDateTime | None = None
    indexed: DoiDateTime | None = None
    created: DoiDateTime | None = None
    published: DoiDateTime | None = None
    published_online: DoiDateTime | None = None
    published_print: DoiDateTime | None = None
    approved: DoiDateTime | None = None

    container_title: str | list[str] | None = None
    original_title: str | list[str] | None = None
    short_title: str | list[str] | None = None
    subtitle: str | list[str] | None = None

    author: Annotated[list[DoiAuthor], Field(default_factory=list)]
    editor: Annotated[list[DoiAuthor], Field(default_factory=list)]
    link: Annotated[list[DoiLink], Field(default_factory=list)]
    assertion: Annotated[list[DoiAssertion], Field(default_factory=list)]
    reference: Annotated[list[DoiReference], Field(default_factory=list)]
    license: Annotated[list[DoiLicense], Field(default_factory=list)]
    funder: Annotated[list[DoiFunder], Field(default_factory=list)]
    updated_by: Annotated[list[DoiUpdatedBy], Field(default_factory=list)]

    # arXiv
    categories: list[str] | None = None
    copyright: str | None = None
    version: str | None = None
    prefix: str | None = None
    source: str | None = None
    id: str | None = None

    alternative_id: Annotated[list[str], Field(default_factory=list)]
    isbn_type: Annotated[list[DoiIsbn], Field(default_factory=list)]
    isbn: Annotated[list[str], Field(default_factory=list)]
    issn: Annotated[list[str], Field(default_factory=list)]

    content_domain: DoiContentDomain | None = None
    journal_issue: DoiJournalIssue | None = None
    standards_body: DoiStandardsBody | None = None

    container_title_short: str | None = None
    publisher_location: str | None = None
    special_numbering: Annotated[str | None,  Field(alias='special_numbering', default=None)]  # Not kebab-case
    edition_number: str | None = None
    article_number: str | None = None
    update_policy: str | None = None
    language: str | None = None
    abstract: str | None = None
    volume: str | None = None
    member: str | None = None
    issue: str | None = None
    page: str | None = None


def parse_doi_json(json_body: str) -> DoiData:
    return DoiData.model_validate_json(json_body, strict=True)
