settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair A = (0, 0);
pair B = (3, 0);
pair C = (1, sqrt(2));

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));
dot(orth_proj(C, A, B - A), L=Label('$O_C$', align=SE));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(C -- orth_proj(C, A, B - A));

markangle(B, A, C, radius=10, L=Label('$\\alpha$'));
markangle(C, orth_proj(C, A, B - A), A, radius=10);
angle_dot(C, orth_proj(C, A, B - A), A, radius=10);
