unitsize(1cm);

import graph;
import geometry;

from notebook access geom, lab;

point O = (0, 0);
point P = (2, 0);
point Q = (5 / 4, 3 / 2);

line g = line(O, P);
line h = line(O, Q);

draw(g, L=Label('$g$', position=0.05, align=S));
draw(h, L=Label('$h$', position=0.95, align=NW));
dot(O,  L=Label('$O$', align=lab.align_oppose(O, Q - P)));
dot(P,  L=Label('$P$', align=S));
dot(-P, L=Label("$P'$", align=N));
dot(Q,  L=Label('$Q$', align=SE));
dot(-Q, L=Label("$Q'$", align=SE));

geom.mark_angle(
  P, O, Q,
  radius=15,
  L=Label('$\\scriptstyle\\angle(\\overrightarrow{OP}, \\overrightarrow{OQ})$'),
  arrow=Arrow(TeXHead)
);

geom.mark_angle(
  -P, O, -Q,
  radius=15,
  L=Label('$\\scriptstyle\\angle(\\overrightarrow{OP\'}, \\overrightarrow{OQ\'})$'),
  arrow=Arrow(TeXHead)
);

draw(
  box(
    -(3P/4 + 3Q/2),
    (3P/4 + 3Q/2)
  ),
  invisible
);
