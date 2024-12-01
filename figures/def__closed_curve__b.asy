unitsize(1.5cm);

import graph;

from notebook access plt;

pair g(real t) {
  return (cos(3t) * cos(t), cos(3t) * sin(t));
}

pair f(real t) {
  return g(t + pi/3 + 1/3);
}

dot(f(0));
draw(
  graph(f, 0, pi),
  marker=plt.arrow_marker(8)
);
