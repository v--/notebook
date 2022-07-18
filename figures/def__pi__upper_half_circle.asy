settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair f(real t) {
  return (-cos(t), sin(t));
}

draw(graph(f, 0, pi), arrow=Arrow(TeXHead));

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-1.5,
  xmax=1.5
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-0.5,
  ymax=1.5
);
