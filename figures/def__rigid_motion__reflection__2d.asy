settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;

real angle = 4;
transform f = (
  0, 0,
  cos(angle), sin(angle),
  sin(angle), -cos(angle)
);

pair v = (
  sqrt(1 / 2 + cos(angle) / 2),
  -sqrt(1 / 2 - cos(angle) / 2)
);

fill(unitsquare, gray);
dot((0.5, 1));
fill(f * unitsquare, mediumgray);
dot(f * (0.5, 1));
draw(v -- -v, dashed);

xaxis(
  xmax=1.2,
  above=true
);

yaxis(
  ymax=1.2,
  above=true
);
