size(15cm, 7cm, keepAspect=false);
unitsize(1cm);

import graph;

from notebook access pens;

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

xaxis(
  axis=BottomTop,
  ticks=Ticks(pTick=pens.thin, extend=true)
);

yaxis(
  axis=LeftRight,
  ticks=Ticks(pTick=pens.thin, extend=true)
);
