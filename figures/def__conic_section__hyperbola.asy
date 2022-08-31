settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

pair f(real t) {
  return (cosh(t), sinh(t));
}

pair g(real t) {
  return (-cosh(t), sinh(t));
}

draw(graph(f, -5pi / 12, 5pi / 12), marker=arrow_marker(2));
draw(graph(g, -5pi / 12, 5pi / 12), marker=arrow_marker(2));

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-2.25,
  xmax=2.25
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-2,
  ymax=2
);
