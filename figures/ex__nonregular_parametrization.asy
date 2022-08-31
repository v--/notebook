settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

pair f(real t) {
  return (t, t^2);
}

dot(f(-1));
draw(
  graph(f, -1, 1),
  marker=arrow_marker(2),
  arrow=Arrow(TeXHead)
);
