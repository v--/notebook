from collections.abc import Sequence  # noqa: TC003
from datetime import datetime  # noqa: TC003
from typing import Annotated

import msgspec
import msgspec.json


FIELD_NAMES_TO_BE_PRESERVED = ['special_numbering']
FIELD_NAMES_TO_BE_CAPITALIZED = ['url', 'doi', 'issn', 'isbn', 'orcid']


def get_doi_field_name(name: str) -> str:
    if name in FIELD_NAMES_TO_BE_PRESERVED:
        return name

    if name in FIELD_NAMES_TO_BE_CAPITALIZED:
        return name.upper()

    return name.replace('_', '-')


class DoiBaseModel(msgspec.Struct, forbid_unknown_fields=True, rename=get_doi_field_name):
    pass


class DoiDateTimePart(msgspec.Struct, array_like=True):
    year: int | None = None
    month: int | None = None
    day: int | None = None


class DoiDateTime(DoiBaseModel):
    date_parts: Annotated[Sequence[DoiDateTimePart], msgspec.Meta(min_length=1)]
    date_time: datetime | None = None
    timestamp: int | None = None
    version: str | None = None


class DoiLicense(DoiBaseModel):
    start: DoiDateTime
    content_version: str
    delay_in_days: int
    url: str


class DoiContentDomain(DoiBaseModel):
    domain: Sequence[str]
    crossmark_restriction: bool


class DoiAffiliation(DoiBaseModel):
    name: str
    place: Sequence[str] = msgspec.field(default_factory=list)


class DoiAuthorRole(DoiBaseModel):
    role: str
    vocabulary: str | None = None


class DoiAuthor(DoiBaseModel):
    name: str | None = None
    family: str | None = None
    given: str | None = None
    suffix: str | None = None
    sequence: str | None = None
    authenticated_orcid: bool | None = None
    orcid: str | None = None
    affiliation: Sequence[DoiAffiliation] | None = None
    role: Sequence[DoiAuthorRole] | None = None


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
    id_type: str
    id: str
    asserted_by: str


class DoiRelationMap(DoiBaseModel):
    is_identical_to: Sequence[DoiRelation] = msgspec.field(default_factory=list)


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

    award: Sequence[str] = msgspec.field(default_factory=list)
    id: Sequence[DoiFunderId] = msgspec.field(default_factory=list)


class DoiStandardsBody(DoiBaseModel):
    name: str
    acronym: str


class DoiUpdatedBy(DoiBaseModel):
    updated: DoiDateTime
    doi: str
    type: str
    label: str
    source: str | None = None


class DoiData(DoiBaseModel):
    publisher: str
    type: str
    doi: str
    url: str
    issued: DoiDateTime
    title: str | Sequence[str]

    resource: DoiResource | None = None
    relation: DoiRelationMap | None = None
    subject: Sequence[DoiSubject] | None = None

    is_referenced_by_count: int | None = None
    references_count: int | None = None
    reference_count: int | None = None
    score: int | None = None

    deposited: DoiDateTime | None = None
    indexed: DoiDateTime | None = None
    created: DoiDateTime | None = None
    published: DoiDateTime | None = None
    published_online: DoiDateTime | None = None
    published_print: DoiDateTime | None = None
    published_other: DoiDateTime | None = None
    approved: DoiDateTime | None = None

    container_title: str | Sequence[str] | None = None
    original_title: str | Sequence[str] | None = None
    short_title: str | Sequence[str] | None = None
    subtitle: str | Sequence[str] | None = None
    event: str | Sequence[str] | None = None
    proceedings_subject: str | Sequence[str] | None = None

    author: Sequence[DoiAuthor] = msgspec.field(default_factory=list)
    editor: Sequence[DoiAuthor] = msgspec.field(default_factory=list)
    link: Sequence[DoiLink] = msgspec.field(default_factory=list)
    assertion: Sequence[DoiAssertion] = msgspec.field(default_factory=list)
    reference: Sequence[DoiReference] = msgspec.field(default_factory=list)
    license: Sequence[DoiLicense] = msgspec.field(default_factory=list)
    funder: Sequence[DoiFunder] = msgspec.field(default_factory=list)
    updated_by: Sequence[DoiUpdatedBy] = msgspec.field(default_factory=list)

    # arXiv
    categories: Sequence[str] | None = None
    copyright: str | None = None
    version: str | None = None
    prefix: str | None = None
    source: str | None = None
    id: str | None = None

    aliases: Sequence[str] = msgspec.field(default_factory=list)
    alternative_id: Sequence[str] = msgspec.field(default_factory=list)
    isbn_type: Sequence[DoiIsbn] = msgspec.field(default_factory=list)
    isbn: Sequence[str] = msgspec.field(default_factory=list)
    issn: Sequence[str] = msgspec.field(default_factory=list)

    content_domain: DoiContentDomain | None = None
    journal_issue: DoiJournalIssue | None = None
    standards_body: DoiStandardsBody | None = None

    container_title_short: str | None = None
    publisher_location: str | None = None
    special_numbering: str | None = None
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
    return msgspec.json.decode(json_body, type=DoiData)
