unitsize(1cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(2.5, 3.5, 4);

line g = tri.AB;
line h = g + (tri.C - tri.B);

draw(tri);
geom.mark_angles(tri);

point A_ = projection(h) * tri.A;
point B_ = projection(h) * tri.B;

dot(tri.A, L=Label('$A$', align=S));
dot(tri.B, L=Label('$B$', align=S));
dot(tri.C, L=Label('$C$', align=N));

dot(A_, L=Label("$A'$", align=N));
dot(B_, L=Label("$B'$", align=N));

draw(tri.A -- A_, dotted);
draw(tri.B -- B_, dotted);

draw(g, L=Label('$g$', align=S, position=0.05));
draw(h, L=Label('$h$', align=N, position=0.05));

geom.mark_angle(
  A_, tri.C, tri.A,
  L=Label('$\\alpha$')
);

geom.mark_angle(
  tri.B, tri.C, B_,
  L=Label('$\\beta$')
);

geom.mark_angle(
  tri.A, tri.C, tri.B,
  L=Label('$\\gamma$')
);

draw(
  box(
    tri.A - (tri.B - tri.A) / 3,
    B_ + (B_ - A_) / 3
  ),
  invisible
);
