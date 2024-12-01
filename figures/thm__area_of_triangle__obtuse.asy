unitsize(1.5cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(3sqrt(2), sqrt(3), 3);
segment oc = altitude(tri.VC);
point OC = foot(tri.VC);

draw(tri);
geom.draw_vertices(tri);

dot(OC, L=Label('$O_C$', align=S));

draw(oc, dashed);
draw(tri.B -- OC, dashed);

geom.mark_angle(tri.B, tri.A, tri.C, L=Label('$\\alpha$'));
geom.mark_angle(tri.A, OC, tri.C);
