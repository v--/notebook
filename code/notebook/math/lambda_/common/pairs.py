from ..parsing import parse_untyped_term


cons = parse_untyped_term('(λx.(λy.(λf.((fx)y))))')
car = parse_untyped_term('(λp.(p(λx.(λy.x))))')
cdr = parse_untyped_term('(λp.(p(λx.(λy.y))))')
