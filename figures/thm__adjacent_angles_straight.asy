usepackage('stix2');
unitsize(1cm);

import geometry;

pair O = (0, 0);
pair P = (2, 0);
pair Q = (-2, 0);
pair R = 2 * (cos(1), sin(1));

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));
draw(O -- R, arrow=Arrow(TeXHead), L=Label('$p$', position=EndPoint));
dot(O, L=Label('$O$', align=S));
