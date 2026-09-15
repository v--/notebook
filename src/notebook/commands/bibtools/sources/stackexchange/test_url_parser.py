from .url_parser import parse_stackexchange_url


def test_parse_short_mo_question_url() -> None:
    parsed = parse_stackexchange_url('https://mathoverflow.net/q/115699')
    assert not parsed.is_answer
    assert parsed.site == 'mathoverflow.net'
    assert parsed.post_id == 115699


def test_parse_full_mo_question_url() -> None:
    parsed = parse_stackexchange_url('https://mathoverflow.net/questions/115699/which-term-is-better-for-the-so-called-sphere-packing')
    assert not parsed.is_answer
    assert parsed.site == 'mathoverflow.net'
    assert parsed.post_id == 115699


def test_parse_short_mo_answer_url() -> None:
    parsed = parse_stackexchange_url('https://mathoverflow.net/a/74013')
    assert parsed.is_answer
    assert parsed.site == 'mathoverflow.net'
    assert parsed.post_id == 74013


def test_parse_full_mo_answer_url() -> None:
    parsed = parse_stackexchange_url('https://mathoverflow.net/questions/74004/what-does-the-σ-in-σ-algebra-stand-for/74013')
    assert parsed.is_answer
    assert parsed.site == 'mathoverflow.net'
    assert parsed.post_id == 74013


def test_parse_short_mathse_question_url() -> None:
    parsed = parse_stackexchange_url('https://math.stackexchange.com/q/873183/229174')
    assert not parsed.is_answer
    assert parsed.site == 'math.stackexchange.com'
    assert parsed.post_id == 873183


def test_parse_full_mathse_question_url() -> None:
    parsed = parse_stackexchange_url('https://math.stackexchange.com/questions/873183/are-variables-logical-or-non-logical-symbols-in-a-logic-system')
    assert not parsed.is_answer
    assert parsed.site == 'math.stackexchange.com'
    assert parsed.post_id == 873183


def test_parse_short_mathse_answer_url() -> None:
    parsed = parse_stackexchange_url('https://math.stackexchange.com/a/2167659/229174')
    assert parsed.is_answer
    assert parsed.site == 'math.stackexchange.com'
    assert parsed.post_id == 2167659


def test_parse_full_mathse_answer_url() -> None:
    parsed = parse_stackexchange_url('https://math.stackexchange.com/questions/2167621/natural-categories-where-monomorphisms-differ-from-injective-morphisms/2167659')
    assert parsed.is_answer
    assert parsed.site == 'math.stackexchange.com'
    assert parsed.post_id == 2167659
