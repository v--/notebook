usepackage('stix2');
unitsize(1cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

pair f(real t) {
  return (t, sqrt(t));
}

pair g(real t) {
  return (t, -sqrt(t));
}

draw(graph(f, 0, 2 / 3 * pi), marker=arrow_marker(2));
draw(graph(g, 0, 2 / 3 * pi), marker=arrow_marker(2));
dot((0, 0));

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-1,
  xmax=3
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-2,
  ymax=2
);
