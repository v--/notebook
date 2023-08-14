usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

int n = 6;

pair drawing_vertex(int k) {
  real a = k / n * 2pi;
  return (cos(a), sin(a));
}

for (int k = 0; k < n; ++k) {
  pair p = drawing_vertex(k);
  dot(p);
  label(string(k + 1), 1.25 * p);
}

draw(
  drawing_vertex(0) -- drawing_vertex(2) -- drawing_vertex(4) -- cycle,
  marker=arrow_marker(3)
);

draw(
  drawing_vertex(1) -- drawing_vertex(3) -- drawing_vertex(5) -- cycle,
  dashed,
  marker=arrow_marker(3)
);
