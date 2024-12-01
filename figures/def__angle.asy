unitsize(1cm);

import geometry;

from notebook access geom;

pair O = (0, 0);
pair P = (9 / 4, 9 / 8);
pair Q = (3 / 4, 3);
pair C = -P * length(Q) - Q * length(P);

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));

geom.mark_angle(
  P, O, Q,
  radius=25,
  L=Label('$\\angle(r, s)$', position=0.6),
  arrow=Arrow(TeXHead)
);

geom.mark_angle(
  Q, O, C,
  p=dashed,
  radius=25,
  L=Label('$\\angle(s, r)$', position=EndPoint),
  arrow=Arrow(TeXHead)
);

geom.mark_angle(
  C, O, P,
  p=dashed,
  radius=25,
  arrow=Arrow(TeXHead)
);
