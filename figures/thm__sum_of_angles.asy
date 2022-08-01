settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair O = (0, 0);
pair P = (9 / 4, 9 / 8);
pair Q = (-5 / 4, 2);
real lambda = 0.7;

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));
draw(O -- lambda * P + (1 - lambda) * Q, arrow=Arrow(TeXHead), L=Label('$p$', position=EndPoint));
dot(O, L=Label('$O$', align=SW));

draw(
  arc(
    O,
    r=1.2,
    angle1=degrees(atan2(P.y, P.x)),
    angle2=degrees(atan2(Q.y, Q.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\alpha + \\beta$', position=0.9)
);

draw(
  arc(
    O,
    r=0.5,
    angle1=degrees(atan2(P.y, P.x)),
    angle2=degrees(atan2(lambda * P.y + (1 - lambda) * Q.y, lambda * P.x + (1 - lambda) * Q.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\alpha$')
);

draw(
  arc(
    O,
    r=0.5,
    angle1=degrees(atan2(lambda * P.y + (1 - lambda) * Q.y, lambda * P.x + (1 - lambda) * Q.x)),
    angle2=degrees(atan2(Q.y, Q.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\beta$')
);
