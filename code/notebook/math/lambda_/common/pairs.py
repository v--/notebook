from ..parsing import parse_pure_term


cons = parse_pure_term('(λx.(λy.(λz.((zx)y))))')
car = parse_pure_term('(λp.(p(λx.(λy.x))))')
cdr = parse_pure_term('(λp.(p(λx.(λy.y))))')
