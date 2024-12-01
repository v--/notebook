usepackage('mathtools');
unitsize(1cm);

import geometry;

from notebook access geom;

currentcoordsys = scale(4) * rotate(5) * defaultcoordsys;

point O = (0, 0);
point A = (1, 0);
point B = (0, 1);
point P = unit((1, 1));

point A_ = projection(Ox(currentcoordsys)) * P;
point B_ = projection(Oy(currentcoordsys)) * P;

draw(O -- A, arrow=Arrow(TeXHead), L=Label('$r$', position=EndPoint));
draw(O -- B, arrow=Arrow(TeXHead));
draw(O -- P, L=Label('$l$', align=NW));
draw(P -- A_, dashed, L=Label('$l \\cdot \\cos(\\rho)$', position=1), align=S);
draw(P -- B_, dashed, L=Label('$l \\cdot \\sin(\\rho)$', position=1), align=W);

dot(O, L=Label('$O$'), align=S);
dot(P, L=Label('$P$'), align=NE);
dot(A_);
dot(B_);

draw(
  arc(
    O,
    r=length(P - O),
    angle1=degrees(atan2(A.y, A.x)) - 15,
    angle2=degrees(atan2(B.y, B.x)) + 15
  ),
  dotted
);

geom.mark_angle(A, O, P, radius=20, L=Label('$\\rho$'), arrow=Arrow(TeXHead));
geom.mark_angle(A, O, B, orth_dot=false);
geom.mark_angle(P, A_, O);
geom.mark_angle(O, B_, P);
