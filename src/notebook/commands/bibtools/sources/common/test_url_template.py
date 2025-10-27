from .url_template import UrlTemplate


def test_url_template_create() -> None:
    identifier = '2011.00412v3'
    url_tool = UrlTemplate('arxiv.org/{identifier}')
    url = url_tool.create(identifier=identifier)
    assert url == 'https://arxiv.org/2011.00412v3'


def test_url_template_extract() -> None:
    identifier = '2011.00412v3'
    url_tool = UrlTemplate('arxiv.org/{identifier}')
    url = url_tool.create(identifier=identifier)
    exctacted = url_tool.extract(url)
    assert exctacted == dict(identifier=identifier)
