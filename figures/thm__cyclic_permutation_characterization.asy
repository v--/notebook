unitsize(1.5cm);

import graph;

from notebook access plt;

int n = 5;

pair f(real t) {
  return (cos(t), sin(t));
}

draw(
  graph(f, 0, 2pi),
  dotted,
  marker=plt.arrow_marker(n)
);


for (int k = 0; k < n; ++k) {
  pair p = f(k / n * 2pi);
  dot(p);
  label('$s_{' + string(k + 1) + '}$', 1.25 * p);
}
