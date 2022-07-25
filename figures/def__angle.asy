settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair O = (0, 0);
pair P = (9 / 4, 9 / 8);
pair Q = (3 / 4, 3);

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));

draw(
  arc(
    O,
    r=0.9,
    angle1=degrees(atan2(P.y, P.x)),
    angle2=degrees(atan2(Q.y, Q.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\sphericalangle(r, s)$', position=0.8, align=NE)
);

draw(
  arc(
    O,
    r=0.9,
    angle1=degrees(atan2(Q.y, Q.x)),
    angle2=180 + degrees(atan2(P.y, P.x))
  ),
  dotted,
  arrow=Arrow(TeXHead)
);

draw(
  arc(
    O,
    r=0.9,
    angle1=180 + degrees(atan2(P.y, P.x)),
    angle2=360 + degrees(atan2(P.y, P.x))
  ),
  dotted,
  arrow=Arrow(TeXHead),
  L=Label('$\\sphericalangle(s, r)$', position=BeginPoint, align=SW)
);
