settings.outformat = 'pdf';

usepackage('stix2');
unitsize(2cm);

import geometry;
import 'asy/angles.asy' as angles;

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 2);

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));
dot((A + B) / 2, L=Label('$M_C$', align=SE));
dot((A + C) / 2, L=Label('$M_B$', align=NW));
dot((B + C) / 2, L=Label('$M_A$', align=NE));
dot((A + B + C) / 3, L=shift(3, 14) * Label('$M$'));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(C -- (A + B) / 2);
draw(A -- (B + C) / 2);
draw(B -- (A + C) / 2);
