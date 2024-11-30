usepackage('stix2');
unitsize(1cm);

import geometry;

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 1.5);
pair D = A + (C - B);

dot(A, L=Label('$A$', align=2SW));
dot(B, L=Label('$B$', align=2SE));
dot(C, L=Label('$C$', align=2NE));
dot(D, L=Label('$D$', align=2NW));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(A -- D, dashed);
draw(C -- D, dashed);
