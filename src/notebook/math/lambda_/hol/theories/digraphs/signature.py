from ....parsing import parse_type
from ...signature import HolSignature, NonLogicalConstantSymbol, SortSymbol


DIRECTED_GRAPH_SIGNATURE = HolSignature(
    SortSymbol('vert'),
    SortSymbol('arc'),
)

DIRECTED_GRAPH_SIGNATURE.add_symbol(NonLogicalConstantSymbol('src', parse_type('(vert → arc)', DIRECTED_GRAPH_SIGNATURE)))
DIRECTED_GRAPH_SIGNATURE.add_symbol(NonLogicalConstantSymbol('dest', parse_type('(vert → arc)', DIRECTED_GRAPH_SIGNATURE)))
