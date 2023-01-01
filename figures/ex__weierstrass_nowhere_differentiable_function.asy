size(15, 7, keepAspect=false);
usepackage('stix2');
unitsize(1cm);

import graph;

real a = 0.9;
real b = 7;
real n = 3;

real f(real x) {
  real result = 0;

  for (int k = 1; k <= n; ++k) {
    result += a^k * cos(b^k * pi * x);
  }

  return result;
}

draw(graph(f, -pi/8, pi/8, n=2500));

pen thin=linewidth(0.1 * linewidth());

xaxis(
  axis=BottomTop,
  ticks=Ticks(pTick=thin, extend=true)
);

yaxis(
  axis=LeftRight,
  ticks=Ticks(pTick=thin, extend=true)
);
