settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair f(real t) {
  return (t, sqrt(t));
}

pair g(real t) {
  return (t, -sqrt(t));
}

draw(graph(f, 0, 2 / 3 * pi), arrow=Arrow(TeXHead));
draw(graph(g, 0, 2 / 3 * pi), arrow=Arrow(TeXHead));
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
