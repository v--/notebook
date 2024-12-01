unitsize(1cm);
size(10cm, 5cm, keepAspect=false);

import graph;

from notebook access pens;

real e = exp(1);

real f_mn(real x, real y) {
  if (y <= x) {
    return 0;
  }

  return 1 - 1 / log(y - x + e);
}

real f_a(real x) {
  return f_mn(0, x);
}

real f_b(real x) {
  return f_mn(x, 100);
}

draw(
  graph(f_a, -10, 110, n=1000),
  L=Label('$f_A$', position=700, align=2N)
);

draw(
  graph(f_b, -10, 110, n=1000),
  L=Label('$f_B$', position=300, align=2N),
  dashed
);

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
