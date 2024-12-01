unitsize(1cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(3, 4, 5);
triangle rfl = triangle(tri.A, tri.B, tri.A + tri.B - tri.C);

draw(tri);
geom.draw_vertices(tri);
geom.mark_angle(tri.A, tri.C, tri.B);

draw(rfl, dashed);
dot(rfl.C, L=Label('$D$', align=S));
geom.mark_angle(rfl.B, rfl.C, rfl.A);
