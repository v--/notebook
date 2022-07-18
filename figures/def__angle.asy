settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair p = (1, 1 / 3);
pair q = (4, 11 / 6);
pair r = (2, 13 / 3);

draw(p -- q, arrow=Arrow(TeXHead));
draw(p -- r, arrow=Arrow(TeXHead));

draw(p -- (p.x, r.y), dotted);
draw((p.x, q.y) -- q, dashed, L=Label('$x_r$', align=N));
draw((p.x, r.y) -- r, dashed, L=Label('$x_s$', align=S));

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
