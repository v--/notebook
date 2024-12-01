import graph;

unitsize(0.75cm);

import graph;

pair f(real x) {
  return (x, 0.0015x^4 - 0.0134x^3 + 0.131x^2 + 0.4722x - 2);
}

draw(f(-5) -- f(-2.5) -- f(0.5) -- f(4), dashed);
dot(f(-5));
dot(f(-2.5));
dot(f(0.5));
dot(f(4));

draw(graph(f, -5, 4));
