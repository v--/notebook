unitsize(1.5cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(sqrt(6), sqrt(3), 3);
segment oc = altitude(tri.VC);
point OC = foot(tri.VC);

draw(tri);
draw(oc);
geom.draw_vertices(tri);

dot(OC, L=Label('$O_C$', align=S));

geom.mark_angle(tri.B, tri.A, tri.C, L=Label('$\\alpha$'));
geom.mark_angle(tri.C, OC, tri.A);
