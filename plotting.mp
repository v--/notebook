def path_of_plot(suffix f)(expr from, to, stp, u) =
  (from, f(from)) * u
  for x = (from + stp) step stp until to:
    --(x, f(x)) * u
  endfor;
enddef;

vardef exp(expr x) =
  mexp(256) ** x
enddef;

vardef ln(expr x) =
  mlog(x) / 256
enddef;
