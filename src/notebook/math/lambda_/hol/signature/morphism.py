import itertools
from typing import override

from notebook.math.lambda_.signature import SignatureMorphism
from notebook.math.lambda_.signature_translation import translate_type

from .exceptions import HolSignatureMorphismError
from .signature import HolSignature
from .symbols import LogicalConstantSymbol, LogicalTypeSymbol, NonLogicalConstantSymbol


class HolSignatureMorphism(SignatureMorphism):
    source: HolSignature

    def __post_init__(self) -> None:
        super().__post_init__()

        for sym in itertools.chain(self.mapping.keys(), self.mapping.values()):
            if isinstance(sym, (LogicalTypeSymbol, LogicalConstantSymbol)):
                raise HolSignatureMorphismError(f'Cannot use {sym.get_kind_string()} symbol {sym}')

    @override
    def get_modified_signature(self) -> HolSignature:
        signature = HolSignature()

        for sort_sym in self.source.iter_sorts():
            signature.add_symbol(self(sort_sym))

        for const_sym in self.source.iter_nonlogical():
            signature.add_symbol(
                NonLogicalConstantSymbol(
                    const_sym.name,
                    translate_type(self, const_sym.type),
                ),
            )

        return signature
