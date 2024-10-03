usepackage('stix2');
unitsize(1cm);
size(10cm, 5cm, keepAspect=false);

import graph;
import 'asymptote/plotting.asy' as plotting;

real f_a(real x) {
  if (x <= 0) {
    return 0;
  }

  return 1 - 1 / log(x + exp(1));
}

draw(graph(f_a, -10, 1000, n=1000), L=Label('$f_A$', position=700, align=2N));

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
