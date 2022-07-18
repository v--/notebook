settings.outformat = 'pdf';

usepackage('stix2');
usepackage('mathtools');
unitsize(1cm);

real t = 1;
pair A = 3 * (0, 0);
pair B = 3 * (cos(t), sin(t));
pair C = 3 * (cos(t), 0);

dot(A, L=Label('$A$', align=W));
label(Label('$\\begin{rcases} \\sin_G(\\alpha) = b / c \\\\ \\cos_G(\\alpha) = a / c \\end{rcases}$', align=W), A + (-0.4, 0));
dot(B, L=Label('$B$', align=E));
label(Label('$\\begin{cases} \\sin_G(\\beta) = a / c \\\\ \\cos_G(\\beta) = b / c \\end{cases}$', align=E), B + (0.35, 0));
dot(C, L=Label('$C$', align=E));

draw(A -- B, L=Label('$c$', align=NW));
draw(A -- C, L=Label('$b$', align=S));
draw(B -- C, L=Label('$a$', align=E));

draw(
  arc(
    A,
    r=0.3,
    angle1=degrees(atan2((B - A).y, (B - A).x)),
    angle2=degrees(atan2((C - A).y, (C - A).x))
  ),
  L=Label('$\\alpha$', position=MidPoint, align=NE)
);

draw(
  arc(
    B,
    r=0.3,
    angle1=degrees(atan2((A - B).y, (A - B).x)),
    angle2=degrees(atan2((C - B).y, (C - B).x))
  ),
  L=Label('$\\beta$', position=MidPoint)
);
