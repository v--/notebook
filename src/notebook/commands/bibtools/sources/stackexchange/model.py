from collections.abc import Sequence

import msgspec
import msgspec.json


class StackExchangeOwner(msgspec.Struct):
    account_id: int
    reputation: int
    user_id: int
    user_type: str
    accept_rate: int
    profile_image: str
    display_name: str
    link: str


class StackExchangePost(msgspec.Struct):
    owner: StackExchangeOwner
    score: int
    last_activity_date: int
    creation_date: int
    question_id: int
    content_license: str


class StackExchangePostResponse(msgspec.Struct):
    has_more: bool
    items: Sequence[StackExchangePost]
    quota_max: int
    quota_remaining: int


class StackExchangeAnswer(StackExchangePost):
    answer_id: int
    is_accepted: bool
    last_edit_date: int | None = None


class StackExchangeAnswerResponse(StackExchangePostResponse):
    items: Sequence[StackExchangeAnswer]


class StackExchangeQuestion(StackExchangePost):
    is_answered: bool
    answer_count: int
    link: str
    title: str
    tags: Sequence[str]
    accepted_answer_id: int | None = None
    last_edit_date: int | None = None


class StackExchangeQuestionResponse(StackExchangePostResponse):
    items: Sequence[StackExchangeQuestion]


def parse_stackexchange_answer_json(json_body: str) -> StackExchangeAnswerResponse:
    return msgspec.json.decode(json_body, type=StackExchangeAnswerResponse)


def parse_stackexchange_question_json(json_body: str) -> StackExchangeQuestionResponse:
    return msgspec.json.decode(json_body, type=StackExchangeQuestionResponse)
