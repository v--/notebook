unitsize(1cm);

import geometry;
from notebook access geom;

triangle tri = triangleabc(3, 4, 4.5);

segment ma = median(tri.VA);
segment mb = median(tri.VB);
segment mc = median(tri.VC);

point M = intersectionpoint(mc, mb);

draw(tri);
geom.draw_segment(ma, LA='$A$', LB='$M_A$');
geom.draw_segment(mb, LA='$B$', LB='$M_B$');
geom.draw_segment(mc, LA='$C$', LB='$M_C$');

dot(M, L=Label('$M$', align=rotate(50) * 2E));
