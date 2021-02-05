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

def path_of_curve(suffix x)(suffix y)(expr from, to, stp, u) =
  (x(from), y(from)) scaled u
  for t = (from + stp) step stp until to:
    --(x(t), y(t)) scaled u
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

vardef cos(expr x) =
  cosd(180 * x / pi)
enddef;

vardef sin(expr x) =
  sind(180 * x / pi)
enddef;

vardef cosh(expr x) =
  (exp(x) + exp(-x)) / 2
enddef;

vardef sin(expr x) =
  sind(180 * x / pi)
enddef;

vardef sinh(expr x) =
  (exp(x) - exp(-x)) / 2
enddef;

pi := 3.14159265358979323846;
