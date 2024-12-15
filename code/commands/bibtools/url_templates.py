from .sources.common.url_template import UrlTemplate


doi =        UrlTemplate('dx.doi.org/{identifier}', r'https?://(dx\.)?doi\.org/(?P<identifier>.+)')
arxiv =      UrlTemplate('arxiv.org/abs/{identifier}')
hal =        UrlTemplate('hal.archives-ouvertes.fr/{identifier}')

eudml =      UrlTemplate('eudml.org/doc/{identifier}')
jstor =      UrlTemplate('www.jstor.org/stable/{identifier}')
handle =     UrlTemplate('hdl.handle.net/{identifier}')
mathnet =    UrlTemplate('mi.mathnet.ru/{identifier}')
mathscinet = UrlTemplate('mathscinet.ams.org/mathscinet-getitem?mr={identifier}')
numdam =     UrlTemplate('www.numdam.org/item/{identifier}')
scopus =     UrlTemplate('www.scopus.com/record/display.url?origin=inward&eid={identifier}')
zbmath =     UrlTemplate('zbmath.org/?q=an:{identifier}')


def clean_identifier(identifier: str | None, template: UrlTemplate) -> str | None:
    if identifier is None:
        return None

    if url_data := template.extract(identifier):
        return url_data['identifier']

    return identifier
