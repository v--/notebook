settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;

transform f = (
  -1.5, -0.5,
  1, 0,
  0, 1
);

fill(unitsquare, gray);
dot((0.5, 1));
fill(f * unitsquare, mediumgray);
dot(f * (0.5, 1));

xaxis(
  xmin=-1.6,
  xmax=1.2,
  above=true
);

yaxis(
  ymin=-0.6,
  ymax=1.2,
  above=true
);
