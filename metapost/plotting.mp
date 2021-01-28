def midpoint = point 0.5 enddef;
def startpoint = point 0 enddef;
def endpoint = point 1 enddef;

def dot = fullcircle scaled 3 enddef;

def path_of_plot(suffix f)(expr from, to, stp, u) =
  (from, f(from)) scaled u
  for x = (from + stp) step stp until to:
    --(x, f(x)) scaled u
  endfor;
enddef;

vardef exp(expr x) =
  mexp(256) ** x
enddef;

vardef ln(expr x) =
  mlog(x) / 256
enddef;

vardef pow(expr x, y) =
  exp(ln(x) * y)
enddef;

pi := 3.14159265358979323846;
