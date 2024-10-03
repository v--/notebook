usepackage('stix2');
unitsize(1cm);

import graph;

real a = 0.9;
real b = 7;
real n = 3;

real f(real t) {
  if (t < -1 || t > 1) {
    return 0;
  }

  return 1 - abs(t);
}

draw(graph(f, -2, 2, n=1000));

pen thin=linewidth(0.1 * linewidth());

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
