unitsize(1.5cm);

import graph;

from notebook access plt;

pair f(real t) {
  return (sin(2t), cos(3t));
}

dot(f(3pi/4));
dot(f(9pi/4));
draw(
  graph(f, 3pi/4, 9pi/4),
  marker=plt.arrow_marker(10)
);
