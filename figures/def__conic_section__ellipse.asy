settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;
import 'asy/plotting.asy' as plotting;

pair f(real t) {
  return (3 / 2 * cos(t), 5 / 4 * sin(t));
}

draw(graph(f, 0, 2pi), marker=arrow_marker(4));
dot((3 / 2, 0));

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-2,
  xmax=2
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-2,
  ymax=2
);
