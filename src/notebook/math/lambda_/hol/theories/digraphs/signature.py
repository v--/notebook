from notebook.math.lambda_.hol.signature import HolSignature, NonLogicalConstantSymbol, SortSymbol
from notebook.math.lambda_.parsing import parse_type


DIRECTED_GRAPH_SIGNATURE = HolSignature(
    SortSymbol('vert'),
    SortSymbol('arc'),
)

DIRECTED_GRAPH_SIGNATURE.add_symbol(NonLogicalConstantSymbol('src', parse_type('(vert → arc)', DIRECTED_GRAPH_SIGNATURE)))
DIRECTED_GRAPH_SIGNATURE.add_symbol(NonLogicalConstantSymbol('dest', parse_type('(vert → arc)', DIRECTED_GRAPH_SIGNATURE)))
