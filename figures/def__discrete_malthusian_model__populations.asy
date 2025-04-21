size(13cm, 8cm, keepAspect=false);
unitsize(1cm);

import graph;

from notebook access pens;

typedef real trajectory(real);
trajectory f(real n0, real alpha) {
  return new real(real x) {
    return n0 * (1 + alpha) ** x;
  };
}

real[] populations = new real[] { 30, 60, 100 };
real alpha = 0.2;
int t_limit = 10;

for (int i = 0; i < populations.length; ++i) {
  draw(
    Label('$n_0 = ' + string(populations[i]) + '$', fontsize(10)),
    graph(f(populations[i], alpha), 0, t_limit, n=t_limit + 1)
  );

  for (int j = 0; j <= t_limit; ++j) {
    dot((j, f(populations[i], alpha)(j)));
  }
}

xaxis(
  Label('$t$'),
  axis=Bottom
);

yaxis(
  Label('$n_t$'),
  axis=Left,
  ticks=Ticks(pTick=pens.thin)
);
