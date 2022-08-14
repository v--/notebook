settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import geometry;
import 'asy/angles.asy' as angles;

pair A = (1, 0);
pair B = (3, 0);
pair C = (1, sqrt(2));
pair Ap = (3, sqrt(2));

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));
dot(Ap, L=Label('$A\'$', align=N));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(Ap -- B, dashed);
draw(Ap -- C, dashed);

markangle(B, A, C, radius=10, L=Label('$\\alpha$'));
angle_dot(B, A, C, radius=10);
