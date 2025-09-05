from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..signature import LambdaSignature
from ..type_system import ExplicitTypeSystem


HOL_SIGNATURE = LambdaSignature(base_types=['o', 'ι'], constant_terms=['Q', 'I'])
HOL = ExplicitTypeSystem(ARROW_ONLY_TYPE_SYSTEM.rules)
