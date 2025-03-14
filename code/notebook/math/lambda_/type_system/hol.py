from ..signature import LambdaSignature
from .explicit import BASE_EXPLICIT_TYPE_SYSTEM, ExplicitTypeSystem


HOL_SIGNATURE = LambdaSignature(base_types=['o', 'ι'], constant_terms=['Q', 'I'])
HOL = ExplicitTypeSystem(BASE_EXPLICIT_TYPE_SYSTEM)
