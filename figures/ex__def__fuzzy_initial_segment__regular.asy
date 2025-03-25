unitsize(1cm);
size(10cm, 5cm, keepAspect=false);

import graph;

from notebook access pens;

real e = exp(1);
int ceiling = 25;

for (int n = 0; n < 30; ++n) {
  pair p = (n, max(0, 1 - n / ceiling));
  dot(p);
}

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
