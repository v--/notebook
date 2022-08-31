settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

pair x = (0, 0);
pair y = (4, 1);

pair f(real t) {
  if (t <= 1) {
    return (1 - t) * y + t * x;
  }

  return (t - 1) * y + (2 - t) * x;
}

pair fp(real t) {
  return f(t) + (0, -1/10);
}

pair fm(real t) {
  return f(t) + (0, 1/10);
}

draw(graph(f, 0, 1));

draw(
  graph(fp, 0, 1),
  dotted,
  marker=arrow_marker(1),
  arrow=Arrow(TeXHead)
);

draw(
  graph(fm, 1, 2),
  dotted,
  marker=arrow_marker(1),
  arrow=Arrow(TeXHead)
);
