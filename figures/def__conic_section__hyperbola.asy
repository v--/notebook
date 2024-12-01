unitsize(1cm);

import graph;

from notebook access plt;

pair f(real t) {
  return (cosh(t), sinh(t));
}

pair g(real t) {
  return (-cosh(t), sinh(t));
}

draw(graph(f, -5pi / 12, 5pi / 12), marker=plt.arrow_marker(2));
draw(graph(g, -5pi / 12, 5pi / 12), marker=plt.arrow_marker(2));

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
