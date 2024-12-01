unitsize(1.5cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(sqrt(6), sqrt(2), 2);
point A_ = tri.B + tri.C - tri.A;

draw(tri);
geom.draw_vertices(tri);

dot(A_, L=Label("$A'$", align=N));
draw(A_ -- tri.B, dashed);
draw(A_ -- tri.C, dashed);

geom.mark_angle(tri.B, tri.A, tri.C, L=Label('$\\alpha$'));
