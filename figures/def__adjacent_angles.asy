unitsize(1cm);

import geometry;

pair O = (0, 0);
pair P = (9 / 4, 9 / 8);
pair Q = (-5 / 4, 2);
real lambda = 0.7;
pair R = lambda * P + (1 - lambda) * Q;

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));
draw(O -- R, arrow=Arrow(TeXHead), L=Label('$p$', position=EndPoint));
dot(O, L=Label('$O$', align=S));
