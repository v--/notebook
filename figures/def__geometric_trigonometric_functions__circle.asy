settings.outformat = 'pdf';

usepackage('stix2');
usepackage('mathtools');
unitsize(1cm);

import graph;

real t = 1;
pair A = 3 * (0, 0);
pair B = 3 * (cos(t), sin(t));
pair C = 3 * (cos(t), 0);

dot(A, L=Label('$(0, 0)$', align=SW));
dot(B, L=Label('$(x_0, y_0)$', align=NE));
dot(C, L=Label('$(x_0, 0)$', align=SE));

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

draw(
  arc(
    A,
    r=3,
    angle1=degrees(-pi / 16),
    angle2=degrees(9 pi / 16)
  )
);

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-1,
  xmax=4
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-1,
  ymax=4
);
