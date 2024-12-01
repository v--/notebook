unitsize(1.5cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(sqrt(3), 3sqrt(2), 3);
segment oc = altitude(tri.VC);
point OC = foot(tri.VC);

draw(tri);
geom.draw_vertices(tri);

dot(OC, L=Label('$O_C$', align=S));

draw(oc, dashed);
draw(tri.B -- OC, dashed);

geom.mark_angle(tri.B, tri.A, tri.C, radius=20, L=Label('$\\alpha$'));
geom.mark_angle(tri.C, OC, tri.A);
