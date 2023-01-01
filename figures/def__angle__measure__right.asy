usepackage('stix2');
usepackage('amsmath');
unitsize(1cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair O = (0, 0);
pair P = (3 / 4, 3);
pair Q = (3, -3 / 4);

draw(O -- P, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- Q, arrow=Arrow(TeXHead), L=Label('$s$', position=EndPoint));

markangle(Label('$\\sphericalangle(r, s) = \\tfrac \\pi 2$'), Q, O, P, radius=15);
angle_dot(Q, O, P, radius=15);
