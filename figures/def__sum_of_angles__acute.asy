unitsize(1cm);

import geometry;

from notebook access geom;

pair O = (0, 0);
pair P = (9 / 4, 9 / 8);
pair Q = (-5 / 4, 2);
real lambda = 0.7;
pair R = lambda * P + (1 - lambda) * Q;

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));
draw(O -- R, arrow=Arrow(TeXHead), L=Label('$p$', position=EndPoint));
dot(O, L=Label('$O$', align=S));

geom.mark_angle(
  P, O, Q,
  radius=40,
  L=Label('$\\alpha + \\beta$', position=0.9),
  arrow=Arrow(TeXHead)
);

geom.mark_angle(
  P, O, R,
  radius=20,
  L=Label('$\\alpha$'),
  arrow=Arrow(TeXHead)
);

geom.mark_angle(
  R, O, Q,
  radius=25,
  L=Label('$\\beta$', align=S),
  arrow=Arrow(TeXHead)
);
