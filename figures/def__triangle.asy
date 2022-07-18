settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

pair A = (0, 0);
pair B = (3, 0);
pair C = (2, 2);

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));

draw(A -- B, L=Label('$c$', align=S));
draw(A -- C, L=Label('$b$', align=NW));
draw(B -- C, L=Label('$a$'));

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
    angle1=degrees(atan2((A - C).y, (A - C).x)),
    angle2=degrees(atan2((B - C).y, (B - C).x))
  ),
  L=Label('$\\gamma$', position=MidPoint)
);

