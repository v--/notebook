# The schema here is extracted from a few example responses and guided by
# https://arxiv.org/schemas/atom.xsd

from dataclasses import dataclass, field

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.models.datatype import XmlDateTime


ARXIV_NAMESPACE = 'http://arxiv.org/schemas/atom'
ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
OPENSEARCH_NAMESPACE = 'http://a9.com/-/spec/opensearch/1.1/'


@dataclass
class ArxivTitle:
    value: str =       field(metadata=dict(type='Text', required=True))
    type: str | None = field(metadata=dict(type='Attribute'), default=None)


@dataclass
class ArxivLink:
    href: str =         field(metadata=dict(type='Attribute', required=True))
    rel: str | None =   field(metadata=dict(type='Attribute'), default=None)
    type: str | None =  field(metadata=dict(type='Attribute'), default=None)
    title: str | None = field(metadata=dict(type='Attribute'), default=None)


@dataclass
class ArxivCategory:
    term: str   =        field(metadata=dict(type='Attribute', required=True))
    scheme: str | None = field(metadata=dict(type='Attribute'), default=None)
    label: str | None =  field(metadata=dict(type='Attribute'), default=None)


@dataclass
class ArxivAuthor:
    name: str = field(metadata=dict(type='Element', required=True))


@dataclass
class ArxivEntry:
    authors: list[ArxivAuthor] =      field(metadata=dict(type='Element', required=True, name='author'))
    links: list[ArxivLink] =          field(metadata=dict(type='Element', required=True, name='link'))
    categories: list[ArxivCategory] = field(metadata=dict(type='Element', required=True, name='category'))
    id: str =                         field(metadata=dict(type='Element', required=True))
    summary: str =                    field(metadata=dict(type='Element', required=True))
    updated: XmlDateTime =            field(metadata=dict(type='Element', required=True))
    published: XmlDateTime =          field(metadata=dict(type='Element', required=True))
    title: ArxivTitle =               field(metadata=dict(type='Element', required=True))

    primary_category: ArxivCategory = field(metadata=dict(type='Element', required=True, namespace=ARXIV_NAMESPACE))
    comment: str | None =             field(metadata=dict(type='Element', namespace=ARXIV_NAMESPACE), default=None)
    affiliation: str | None =         field(metadata=dict(type='Element', namespace=ARXIV_NAMESPACE), default=None)
    journal_ref: str | None =         field(metadata=dict(type='Element', namespace=ARXIV_NAMESPACE), default=None)
    doi: str | None =                 field(metadata=dict(type='Element', namespace=ARXIV_NAMESPACE), default=None)


@dataclass
class ArxivFeed:
    class Meta:
        namespace = ATOM_NAMESPACE
        name = 'feed'

    id: str =                   field(metadata=dict(type='Element', required=True))
    updated: XmlDateTime =      field(metadata=dict(type='Element', required=True))
    link: ArxivLink =           field(metadata=dict(type='Element', required=True))
    title: ArxivTitle =         field(metadata=dict(type='Element', required=True))
    total_results: int =        field(metadata=dict(type='Element', required=True, namespace=OPENSEARCH_NAMESPACE, name='totalResults'))
    start_index: int =          field(metadata=dict(type='Element', required=True, namespace=OPENSEARCH_NAMESPACE, name='startIndex'))
    items_per_page: int =       field(metadata=dict(type='Element', required=True, namespace=OPENSEARCH_NAMESPACE, name='itemsPerPage'))
    entries: list[ArxivEntry] = field(metadata=dict(type='Element', name='entry'), default_factory=list)


def parse_arxiv_xml(xml_body: str) -> ArxivFeed:
    parser = XmlParser()
    return parser.from_string(xml_body, ArxivFeed)
