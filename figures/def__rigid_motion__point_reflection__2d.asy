settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;

real angle = 4;
pair O = (-0.1, -0.1);
transform f = (
  2O.x, 2O.y,
  -1, 0,
  0, -1
);

fill(unitsquare, gray);
dot((0.5, 1));
fill(f * unitsquare, mediumgray);
dot(f * (0.5, 1));
dot(O);

xaxis(
  xmax=1.2,
  above=true
);

yaxis(
  ymax=1.2,
  above=true
);
