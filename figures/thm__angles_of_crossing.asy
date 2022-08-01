settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair O = (0, 0);
pair P = (2, 0);
pair Q = (5 / 4, 3 / 2);

path g = (-3, 0) -- (3, 0);
path h = (-5 / 3, -2) -- (5 / 3, 2);

draw(g, L=Label('$g$', position=0.05, align=S));
draw(h, L=Label('$h$', position=0.9, align=NW));
dot(O, L=Label('$O$', align=S));
dot(P, L=Label('$P$', align=S));
dot(-P, L=Label('$P\'$', align=N));
dot(Q, L=Label('$Q$', align=SE));
dot(-Q, L=Label('$Q\'$', align=SE));

draw(
  arc(
    O,
    r=0.6,
    angle1=degrees(atan2(P.y, P.x)),
    angle2=degrees(atan2(Q.y, Q.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OP}, \\overrightarrow{OQ})$', position=0.25, align=NE)
);

draw(
  arc(
    O,
    r=0.6,
    angle1=degrees(atan2(-Q.y, -Q.x)),
    angle2=degrees(atan2(P.y, P.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OQ\'}, \\overrightarrow{OP})$', position=0.5, align=SE)
);

draw(
  arc(
    O,
    r=0.6,
    angle1=degrees(atan2(-P.y, -P.x)),
    angle2=degrees(atan2(-Q.y, -Q.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OP\'}, \\overrightarrow{OQ\'})$', position=0.25, align=SW)
);

draw(
  arc(
    O,
    r=0.6,
    angle1=degrees(atan2(Q.y, Q.x)),
    angle2=degrees(atan2(P.y, -P.x))
  ),
  arrow=Arrow(TeXHead),
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OQ}, \\overrightarrow{OP\'})$', position=0.5, align=NW)
);
