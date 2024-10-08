usepackage('stix2');
unitsize(1cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

real f(real t) {
  if (t < -1 || t > 1) {
    return 0;
  }

  return 1 - abs(t);
}

draw(graph(f, -2, 2, n=1000));

xaxis(
  axis=Bottom,
  p=thin,
  ticks=Ticks(pTick=thin)
);

yaxis(
  axis=Left,
  p=thin,
  ticks=Ticks(pTick=thin)
);
