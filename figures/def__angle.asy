settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair v0 = (1, 1 / 3);
pair v1 = (4, 11 / 6);
pair v2 = (2, 13 / 3);

draw(v0 -- v1, arrow=Arrow(TeXHead));
draw(v0 -- v2, arrow=Arrow(TeXHead));

draw(v0 -- (v0.x, v2.y), dotted);
draw((v0.x, v1.y) -- v1, dashed, L=Label('$x_1$', align=N));
draw((v0.x, v2.y) -- v2, dashed, L=Label('$x_2$', align=S));

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-0.2
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-0.2
);
