settings.outformat = 'pdf';

usepackage('stix2');
usepackage('mathtools');
unitsize(1cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair O = (0, 0);
pair A = (4, -0.5);
pair B = (0.5, 4);
pair P = (2, 2);

draw(O -- A, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- B, arrow=Arrow(TeXHead));
draw(O -- P, L=Label('$l$', align=NW));
draw(P -- orth_proj(P, O, A), dashed, L=Label('$l \\cdot \\cos(\\rho)$', position=1), align=S);
draw(P -- orth_proj(P, O, B), dashed, L=Label('$l \\cdot \\sin(\\rho)$', position=1), align=W);

dot(O, L=Label('$O$'), align=S);
dot(P, L=Label('$P$'), align=NE);
dot(orth_proj(P, O, A));
dot(orth_proj(P, O, B));

draw(
  arc(
    O,
    r=length(P - O),
    angle1=degrees(atan2(A.y, A.x)) - 15,
    angle2=degrees(atan2(B.y, B.x)) + 15
  ),
  dotted
);

markangle(A, O, P, radius=20, L=Label('$\\rho$'), arrow=Arrow(TeXHead));

markangle(A, O, B, radius=10);
angle_dot(A, O, P, radius=10);

markangle(P, orth_proj(P, O, A), O, radius=10);
angle_dot(P, orth_proj(P, O, A), O, radius=10);

markangle(O, orth_proj(P, O, B), P, radius=10);
angle_dot(O, orth_proj(P, O, B), P, radius=10);
