usepackage('stix2');
unitsize(1cm);

import graph;

pair f(real t) {
  return (t, t * t);
}

draw(graph(f, -1.25, 1.25));
draw(graph(f, 0.15, 1), linewidth(1.5pt));
dot(f(0.15), L=Label('$(x, y)$'), align=S);
dot(f(1), L=Label('$(x + t, y + t^2)$'), align=E);
