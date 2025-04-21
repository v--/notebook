size(13cm, 8cm, keepAspect=false);
unitsize(1cm);

import graph;

from notebook access pens;

typedef real trajectory(real);
trajectory f(real n_0, real a, real b) {
  return new real(real x) {
    real result = n_0;

    for (int t = 1; t <= x; ++t) {
      result = result * (1 + a - b * result);
    }

    return result;
  };
}

int t_limit = 20;
real a = 0.2;
real b = 0.002;
real[] populations = new real[] { 50, 100, 150 };

for (int i = 0; i < populations.length; ++i) {
  real n_0 = populations[i];

  draw(
    Label('$n_0 = ' + string(n_0) + '$'),
    graph(f(n_0, a, b), 0, t_limit, n=t_limit)
  );

  for (int j = 0; j <= t_limit; ++j) {
    dot((j, f(n_0, a, b)(j)));
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
