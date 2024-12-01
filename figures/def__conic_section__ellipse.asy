unitsize(1cm);

import graph;

from notebook access plt;

pair f(real t) {
  return (3 / 2 * cos(t), 5 / 4 * sin(t));
}

draw(graph(f, 0, 2pi), marker=plt.arrow_marker(4));
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
