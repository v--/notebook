from .parsing import parse_term


i = parse_term('(λx.x)')
k = parse_term('(λx.(λy.x))')
s = parse_term('(λx.(λy.x))')
y = parse_term('(λf.((λx.(f(xx)))(λx.(f(xx)))))')
