unitsize(1.5cm);

import graph;

from notebook access plt;

pair f(real t) {
  return (t, t^2);
}

dot(f(-1));
draw(
  graph(f, -1, 1),
  marker=plt.arrow_marker(2),
  arrow=Arrow(TeXHead)
);
