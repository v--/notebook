usepackage('stix2');
unitsize(1.3cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/point_lattices.asy' as point_lattices;

pair o = (0, 0);
pair u = (1, 0) / 2;
pair v = (1, -sqrt(3)) / 4;
path circ = scale(0.1) * unitcircle;

string[] labels = new string[] { 'Monad', 'Dyad', 'Triad', 'Tetrad' };

int n = 4;

for (int a = 0; a < n; ++a) {
  for (int b = 0; b <= a; ++b) {
    dot(a * u - b * v);
  }

  label(n * u + (n - 1 - a) * (0, -v.y), labels[a], align=E);
}
