usepackage('stix2');
unitsize(1cm);

import graph;

pair f(real t) {
  return (t, t * t);
}

pair d(real t) {
  return (1, 2t);
}

void draw_tangent(real t) {
  pair d = unit((1, 2t));
  draw(f(t) - 3d/2 -- f(t) + 3d/2, gray);
  dot(f(t), gray);
}

draw(graph(f, -1.25, 1.25), linewidth(1.5pt));
draw_tangent(-1);
draw_tangent(0);
draw_tangent(1/2);
