from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, alias_generators


class GoogleBookBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        extra='forbid'
    )


class GoogleBookIndustryIdentifier(GoogleBookBaseModel):
    type: str
    identifier: str



class GoogleBookVolumeInfo(GoogleBookBaseModel):
    industry_identifiers: list[GoogleBookIndustryIdentifier]
    title: str
    language: str
    authors: list[str] | None = None
    published_date: str | None = None
    subtitle: str | None = None
    publisher: str | None = None
    description: str | None = None



class GoogleBookSearchInfo(GoogleBookBaseModel):
    text_snippet: str



class GoogleBook(GoogleBookBaseModel):
    volume_info: GoogleBookVolumeInfo
    search_info: GoogleBookSearchInfo | None = None



class GoogleBooksResponse(GoogleBookBaseModel):
    items: Annotated[list[GoogleBook], Field(default_factory=list)]


def parse_isbn_json(json_body: str) -> GoogleBooksResponse:
    return GoogleBooksResponse.model_validate_json(json_body)
