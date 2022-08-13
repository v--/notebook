settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;
import geometry;

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

markangle(
  P, O, Q,
  radius=15,
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OP}, \\overrightarrow{OQ})$'),
  arrow=Arrow(TeXHead)
);

markangle(
  -Q, O, P,
  radius=15,
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OQ\'}, \\overrightarrow{OP})$'),
  arrow=Arrow(TeXHead)
);

markangle(
  -P, O, -Q,
  radius=15,
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OP\'}, \\overrightarrow{OQ\'})$'),
  arrow=Arrow(TeXHead)
);

markangle(
  Q, O, -P,
  radius=15,
  L=Label('$\\scriptstyle\\sphericalangle(\\overrightarrow{OQ}, \\overrightarrow{OP\'})$'),
  arrow=Arrow(TeXHead)
);
