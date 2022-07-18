settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair O = (0, 0);
pair u = (2, 1);
pair v = (-1 / 3, -3 / 2);

draw(O -- u, dashed, arrow=Arrow(TeXHead), L=Label('$u$', align=N));
draw(O -- v, dashed, arrow=Arrow(TeXHead), L=Label('$v$'));
draw(O -- (u + v), dashed, arrow=Arrow(TeXHead), L=Label('$u + v$', align=S));

xaxis(arrow=Arrow(TeXHead));
yaxis(arrow=Arrow(TeXHead));
