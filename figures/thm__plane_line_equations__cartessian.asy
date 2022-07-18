settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

path l = (-1, -2) -- (2, 3 / 2);
draw(l, L=Label('$y = kx + m$', position=BeginPoint), align=S);

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-2,
  xmax=2
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-2,
  ymax=2
);
