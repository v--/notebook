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

real[] rates = new real[] { -0.2, 0, 0.1, 0.2 };
real n_0 = 100;
int t_limit = 10;

for (int i = 0; i < rates.length; ++i) {
  draw(
    Label('$\\alpha = ' + string(rates[i]) + '$'),
    graph(f(n_0, rates[i]), 0, t_limit, n=t_limit + 1)
  );

  for (int j = 0; j <= t_limit; ++j) {
    dot((j, f(n_0, rates[i])(j)));
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
