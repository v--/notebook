settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair f(real t) {
  return (3 / 2 * cos(t), 5 / 4 * sin(t));
}

draw(graph(f, -pi / 4, 3 / 4 * pi), arrow=Arrow(TeXHead));
draw(graph(f, 3 / 4 * pi, 7 / 4 * pi), arrow=Arrow(TeXHead));
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
