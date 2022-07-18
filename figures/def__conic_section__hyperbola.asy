settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair f(real t) {
  return (cosh(t), sinh(t));
}

pair g(real t) {
  return (-cosh(t), sinh(t));
}

draw(graph(f, -5 / 12 * pi, -pi / 6), arrow=Arrow(TeXHead));
draw(graph(f, -pi / 6, 5 / 12 * pi), arrow=Arrow(TeXHead));
draw(graph(g, -5 / 12 * pi, -pi / 6), arrow=Arrow(TeXHead));
draw(graph(g, -pi / 6, 5 / 12 * pi), arrow=Arrow(TeXHead));

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
