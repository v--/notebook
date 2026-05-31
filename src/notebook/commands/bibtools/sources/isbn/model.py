from collections.abc import Sequence  # noqa: TC003

from pydantic import BaseModel, ConfigDict, Json


class OLBaseModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class OLBookType(OLBaseModel):
    key: str


class OLBookLanguage(OLBaseModel):
    key: str


class OLBookAuthor(OLBaseModel):
    key: str
    name: str


class OLBookWork(OLBaseModel):
    key: str


class OLBookDate(OLBaseModel):
    type: str
    value: str


class OLBookNote(OLBaseModel):
    type: str
    value: str
    model_type: str | None = None


class OLBookDescription(OLBaseModel):
    type: str
    value: str


class OLBookIdentifiers(OLBaseModel):
    goodreads: Sequence[str] | None = None
    librarything: Sequence[str] | None = None


class OLBookToCEntryType(OLBaseModel):
    key: str


class OLBookToCEntry(OLBaseModel):
    type: OLBookToCEntryType
    level: int
    title: str
    label: str | None = None
    pagenum: str | None = None


class OLBookClassifications(OLBaseModel):
    pass


class OLBookDetails(OLBaseModel):
    created: OLBookDate
    key: str
    languages: Sequence[OLBookLanguage]
    last_modified: OLBookDate
    latest_revision: int
    number_of_pages: int
    publish_date: str
    publishers: Sequence[str]
    revision: int
    source_records: Sequence[str]
    title: str
    type: OLBookType
    authors: Sequence[OLBookAuthor] | None = None
    by_statement: str | None = None
    classifications: OLBookClassifications | None = None
    contributions: Sequence[str] | None = None
    covers: Sequence[int] | None = None
    description: OLBookDescription | None = None
    dewey_decimal_class: Sequence[str] | None = None
    edition_name: str | None = None
    genres: Sequence[str] | None = None
    identifiers: OLBookIdentifiers | None = None
    isbn_10: Sequence[str] | None = None
    isbn_13: Sequence[str] | None = None
    lc_classifications: Sequence[str] | None = None
    lccn: Sequence[str] | None = None
    local_id: Sequence[str] | None = None
    notes: OLBookNote | str | None = None
    ocaid: str | None = None
    oclc_numbers: Sequence[str] | None = None
    pagination: str | None = None
    physical_dimensions: str | None = None
    physical_format: str | None = None
    publish_country: str | None = None
    publish_places: Sequence[str] | None = None
    series: Sequence[str] | None = None
    subjects: Sequence[str] | None = None
    subtitle: str | None = None
    table_of_contents: Sequence[OLBookToCEntry] | None = None
    uri_descriptions: Sequence[str] | None = None
    uris: Sequence[str] | None = None
    url: Sequence[str] | None = None
    weight: str | None = None
    work_titles: Sequence[str] | None = None
    works: Sequence[OLBookWork]


class OLBook(OLBaseModel):
    bib_key: str
    info_url: str
    preview: str
    preview_url: str
    thumbnail_url: str
    details: OLBookDetails


def parse_isbn_json(json: Json) -> OLBook:
    return OLBook.model_validate(json)
