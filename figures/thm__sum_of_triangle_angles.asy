settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 2);
pair Ap = (A.x, C.y);
pair Bp = (B.x, C.y);

dot(A, L=Label('$A$', align=SW));
dot(Ap, L=Label('$A\'$', align=N));
dot(B, L=Label('$B$', align=SE));
dot(Bp, L=Label('$B\'$', align=N));
dot(C, L=Label('$C$', align=N));

draw(A -- C);
draw(A -- Ap, dotted);
draw(B -- C);
draw(B -- Bp, dotted);

draw((-2, 0) -- (5, 0), L=Label('$g$', align=S, position=0.1));
draw((-2, 2) -- (5, 2), L=Label('$h$', align=N, position=0.1));

draw(
  arc(
    A,
    r=0.3,
    angle1=degrees(atan2((B - A).y, (B - A).x)),
    angle2=degrees(atan2((C - A).y, (C - A).x))
  ),
  L=Label('$\\alpha$', position=MidPoint)
);

draw(
  arc(
    C,
    r=0.3,
    angle1=degrees(atan2((Ap - C).y, (Ap - C).x)) - 360,
    angle2=degrees(atan2((A - C).y, (A - C).x))
  ),
  L=Label('$\\alpha$', position=MidPoint)
);

draw(
  arc(
    B,
    r=0.3,
    angle1=degrees(atan2((C - B).y, (C - B).x)),
    angle2=degrees(atan2((A - B).y, (A - B).x))
  ),
  L=Label('$\\beta$', position=MidPoint)
);

draw(
  arc(
    C,
    r=0.3,
    angle1=degrees(atan2((B - C).y, (B - C).x)),
    angle2=degrees(atan2((Bp - C).y, (Bp - C).x))
  ),
  L=Label('$\\beta$', position=MidPoint)
);

draw(
  arc(
    C,
    r=0.3,
    angle1=degrees(atan2((A - C).y, (A - C).x)),
    angle2=degrees(atan2((B - C).y, (B - C).x))
  ),
  L=Label('$\\gamma$', position=MidPoint)
);
