usepackage('stix2');
unitsize(1.5cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair A = (0, 0);
pair B = (3, 0);
pair C = (1, sqrt(2));
pair D = A + B - C;

dot(A, L=Label('$A$', align=W));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));
dot(D, L=Label('$D$', align=S));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(A -- D, dashed);
draw(B -- D, dashed);

markangle(Label('$\\alpha$'), B, A, C, radius=15);
markangle(Label('$\\beta$'), C, B, A, radius=15);
markangle(Label('$\\gamma$'), A, C, B, radius=10);
angle_dot(A, C, B, radius=10);

markangle(Label('$\\alpha$'), A, B, D, radius=15);
markangle(Label('$\\beta$'), D, A, B, radius=15);
markangle(Label('$\\gamma$'), B, D, A, radius=10);
angle_dot(B, D, A, radius=10);
