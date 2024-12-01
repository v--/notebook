unitsize(1.5cm);

import geometry;

from notebook access geom, lab;

point A = (0, 0);
point B = (3, 0);
point C = (2, 2);

triangle tri = triangleabc(sqrt(5), 2sqrt(2), 3);

segment oa = altitude(tri.VA);
segment ob = altitude(tri.VB);
segment oc = altitude(tri.VC);

point OA = foot(tri.VA);
point OB = foot(tri.VB);
point OC = foot(tri.VC);

point O = orthocenter(tri);

draw(tri);
draw(oa);
draw(ob);
draw(oc);
geom.draw_vertices(tri);

dot(OA, L=Label('$O_A$', align=lab.align_oppose(OA, O)));
dot(OB, L=Label('$O_B$', align=lab.align_oppose(OB, O)));
dot(OC, L=Label('$O_C$', align=lab.align_oppose(OC, O)));
dot(O, L=Label('$O$', align=1W + 1.5S));

geom.mark_angle(B, OB, C, radius=7);
geom.mark_angle(C, OA, A, radius=7);
geom.mark_angle(C, OC, A, radius=7);
