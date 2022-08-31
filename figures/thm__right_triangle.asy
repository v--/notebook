settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair A = (0, 0);
pair B = (3, 0);
pair C = (1, sqrt(2));

dot(A, L=Label('$A$', align=W));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));

draw(A -- B);
draw(A -- C);
draw(B -- C);

markangle(Label('$\\alpha$'), B, A, C, radius=10);
markangle(Label('$\\beta$'), C, B, A, radius=15);
markangle(Label('$\\gamma$'), A, C, B, radius=10);
angle_dot(A, C, B, radius=10);
