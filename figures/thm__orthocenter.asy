usepackage('stix2');
unitsize(1.5cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 2);

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));
dot(orth_proj(C, A, B - A), L=Label('$O_C$', align=SE));
dot(orth_proj(B, A, C - A), L=Label('$O_B$', align=NW));
dot(orth_proj(A, B, C - B), L=Label('$O_A$', align=NE));
dot((2, 1), L=shift(-18, 1) * Label('$O$'));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(C -- orth_proj(C, A, B - A));
draw(A -- orth_proj(A, B, C - B));
draw(B -- orth_proj(B, A, C - A));

markangle(B, orth_proj(C, A, B - A), C, radius=7);
angle_dot(B, orth_proj(C, A, B - A), C, radius=7);

markangle(C, orth_proj(A, B, C - B), A, radius=7);
angle_dot(C, orth_proj(A, B, C - B), A, radius=7);

markangle(A, orth_proj(B, A, C - A), B, radius=7);
angle_dot(A, orth_proj(B, A, C - A), B, radius=7);
