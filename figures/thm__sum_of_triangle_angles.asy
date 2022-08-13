settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import geometry;

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 2);
pair Ap = (A.x, C.y);
pair Bp = (B.x, C.y);

dot(A, L=Label('$A$', align=SW));
dot(Ap, L=Label('$A\'$', align=N));
dot(B, L=Label('$B$', align=SE));
dot(Bp, L=Label('$B\'$', align=N));
dot(C, L=Label('$C$', align=N));

draw(A -- C);
draw(A -- Ap, dotted);
draw(B -- C);
draw(B -- Bp, dotted);

draw((-2, 0) -- (5, 0), L=Label('$g$', align=S, position=0.1));
draw((-2, 2) -- (5, 2), L=Label('$h$', align=N, position=0.1));

markangle(
  B, A, C,
  radius=10,
  L=Label('$\\alpha$')
);

markangle(
  Ap, C, A,
  radius=10,
  L=Label('$\\alpha$')
);

markangle(
  C, B, A,
  radius=10,
  L=Label('$\\beta$')
);

markangle(
  B, C, Bp,
  radius=10,
  L=Label('$\\beta$')
);

markangle(
  A, C, B,
  radius=10,
  L=Label('$\\gamma$')
);
