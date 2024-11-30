usepackage('stix2');
unitsize(1.5cm);

import geometry;

import 'asymptote/pens.asy' as pens;
import 'asymptote/angles.asy' as angles;

point A = (1, 0);
point B = (2, -1.5);
point M = (A + B) / 2;

line MP = perpendicular(M, line(A, B));
point P = intersectionpoint(MP, Ox);

dot(A, L=Label('$A$', align=N));
dot(B, L=Label('$B$', align=S));
dot(M, L=Label('$M$', align=2S + 0.5W));
dot(P, L=Label('$P$', align=SE));

draw(A -- B);
draw(A -- P);
draw(B -- P);

draw(MP);

markangle(B, M, P, radius=10);
angle_dot(B, M, P, radius=10);

point upper_right = relpoint(MP, 2.5);
point lower_left = relpoint(MP, -2.5);
draw(box(lower_left, upper_right), invisible);

newpage();

dot(A, L=Label('$A$', align=2N));
dot(B, L=Label('$B$', align=2S));

draw(MP);
fill(lower_left -- upper_right -- (lower_left.x, upper_right.y) -- cycle, right_hatch + opacity(0.3));
fill(lower_left -- upper_right -- (upper_right.x, lower_left.y) -- cycle, left_hatch + opacity(0.3));
