# ruff: noqa: N815

from dataclasses import dataclass, field

from xsdata.formats.dataclass.parsers import JsonParser


@dataclass
class GoogleBookIndustryIdentifier:
    type: str
    identifier: str


@dataclass
class GoogleBookVolumeInfo:
    industryIdentifiers: list[GoogleBookIndustryIdentifier]
    title: str
    language: str
    authors: list[str] = field(default_factory=list)
    publishedDate: str | None = None
    subtitle: str | None = None
    publisher: str | None = None
    description: str | None = None


@dataclass
class GoogleBookSearchInfo:
    textSnippet: str


@dataclass
class GoogleBook:
    volumeInfo: GoogleBookVolumeInfo
    searchInfo: GoogleBookSearchInfo | None = None


@dataclass
class GoogleBooksResponse:
    items: list[GoogleBook] = field(metadata=dict(type='Element'), default_factory=list)


def parse_isbn_json(json_body: str) -> GoogleBooksResponse:
    parser = JsonParser()
    return parser.from_string(json_body, GoogleBooksResponse)
