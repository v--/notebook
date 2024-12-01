unitsize(1cm);

import geometry;

from notebook access geom, lab, pens;

triangle tri = triangleabc(4, 4, 4);

segment ma = median(tri.VA);
segment mb = median(tri.VB);
segment mc = median(tri.VC);

point M = intersectionpoint(mc, mb);

fill(tri.A -- mc.B -- tri.C -- cycle, pens.nw_hatch);
fill(tri.A -- mb.B -- tri.B -- cycle, pens.ne_hatch);

draw(tri);
geom.draw_segment(ma, LA='$A$', LB='$M_A$');
geom.draw_segment(mb, LA='$B$', LB='$M_B$');
geom.draw_segment(mc, LA='$C$', LB='$M_C$');

dot(M, L=Label('$M$', align=rotate(63) * 2.5E));
