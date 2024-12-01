unitsize(1cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(3, 4.5, 5);
triangle rfl = triangle(tri.A, tri.A + tri.C - tri.B, tri.C);

draw(tri);
geom.draw_vertices(tri);

draw(rfl, dashed);
dot(rfl.B, L=Label('$D$', align=W));
