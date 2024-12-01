unitsize(1cm);

import graph;

from notebook access pens;

real f(real t) {
  if (t < -1 || t > 1) {
    return 0;
  }

  return 1 - abs(t);
}

draw(graph(f, -2, 2, n=1000));

xaxis(
  axis=Bottom,
  p=pens.thin,
  ticks=Ticks(pTick=pens.thin)
);

yaxis(
  axis=Left,
  p=pens.thin,
  ticks=Ticks(pTick=pens.thin)
);
