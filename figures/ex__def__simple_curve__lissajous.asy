settings.outformat = 'pdf';

usepackage('amsmath');
usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asymptote/plotting.asy' as plotting;

pair f(real t) {
  return (sin(2t), cos(3t));
}

draw(
  graph(f, pi/2 - 1/2, pi/2 + 1/2),
  marker=arrow_marker(4)
);

draw(
  graph(f, 3pi/2 - 1/2, 3pi/2 + 1/2),
  marker=arrow_marker(4)
);

dot(f(pi/2 - 1/2),  align=SE, L=Label('$0 < t < \\dfrac \\pi 2$'));
dot(f(pi/2 + 1/2),  align=NW, L=Label('$\\dfrac \\pi 2 < t < \\pi$'));
dot(f(3pi/2 + 1/2), align=SW, L=Label('$\\pi < t < \\dfrac {3\\pi} 2$'));
dot(f(3pi/2 - 1/2), align=NE, L=Label('$\\dfrac {3\\pi} 2 < t < 2\\pi$'));

xaxis(
  arrow=Arrow(TeXHead),
  L=Label('$\\sin(2t)$'),
  xmin=-3,
  xmax=3
);

yaxis(
  arrow=Arrow(TeXHead),
  L=Label('$\\cos(3t)$'),
  autorotate=false,
  ymin=-2,
  ymax=2
);
