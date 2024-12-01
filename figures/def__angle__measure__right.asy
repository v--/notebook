usepackage('amsmath');
unitsize(1cm);

import geometry;
from notebook access geom;

pair O = (0, 0);
pair P = (3 / 4, 3);
pair Q = (3, -3 / 4);

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));

geom.mark_angle(Q, O, P, radius=15, L=Label('$\\angle(r, s) = \\tfrac \\pi 2$'));
