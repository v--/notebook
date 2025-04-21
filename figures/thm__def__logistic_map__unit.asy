unitsize(4cm);

import graph;

from notebook access pens;

real a = 4;
real f(real x) {
  return a * x * (1 - x);
};

draw(graph(f, 0, 1));

xaxis(
  Label('$x$'),
  axis=Bottom,
  ticks=Ticks(pTick=pens.thin)
);

yaxis(
  Label('$f(x)$'),
  axis=Left,
  ticks=Ticks(pTick=pens.thin)
);
