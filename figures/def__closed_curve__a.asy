settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asy/plotting.asy' as plotting;

pair g(real t) {
  return (cos(3t) * cos(t), cos(3t) * sin(t));
}

pair f(real t) {
  return g(t + 1/3);
}

dot(f(0));
draw(
  graph(f, 0, pi),
  marker=arrow_marker(8)
);
