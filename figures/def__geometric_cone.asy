settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;

real angle = 2.5;
transform f = (
  0, 0,
  cos(angle), -sin(angle),
  sin(angle), cos(angle)
);

draw((0, 0) -- (1, 0.5), arrow=Arrow(TeXHead));
draw((0, 0) -- (0.5, 1), arrow=Arrow(TeXHead));
draw((0, 0) -- (-1, -0.5), arrow=Arrow(TeXHead));
draw((0, 0) -- (-0.5, -1), arrow=Arrow(TeXHead));
fill((0, 0) -- (-0.5, -1) -- (-1, -1) -- (-1, -0.5) -- cycle, opacity(0.3));

xaxis(
  above=true
);

yaxis(
  above=true
);
