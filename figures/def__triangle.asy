usepackage('stix2');
unitsize(1cm);

import geometry;

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 2);

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));

draw(A -- B);
draw(A -- C);
draw(B -- C);

markangle(
  B, A, C,
  radius=10,
  L=Label('$\\alpha$')
);

markangle(
  C, B, A,
  radius=10,
  L=Label('$\\beta$')
);

markangle(
  A, C, B,
  radius=10,
  L=Label('$\\gamma$')
);
