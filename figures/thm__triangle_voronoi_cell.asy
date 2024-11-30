usepackage('stix2');
unitsize(1cm);

import geometry;

import 'asymptote/geom/segment.asy' as segment;
import 'asymptote/geom/tri.asy' as tri;
import 'asymptote/labels.asy' as labels;
import 'asymptote/pens.asy' as pens;

triangle tri = triangleabc(4, 4, 4);

segment ma = median(tri.VA);
segment mb = median(tri.VB);
segment mc = median(tri.VC);

point M = intersectionpoint(mc, mb);

draw(tri);
draw_segment(ma, LA='$A$', LB='$M_A$');
draw_segment(mb, LA='$B$', LB='$M_B$');
draw_segment(mc, LA='$C$', LB='$M_C$');

dot(M, L=Label('$M$', align=rotate(63) * 2.5E));

fill(tri.A -- mc.B -- tri.C -- cycle, right_hatch + opacity(0.3));
fill(tri.A -- mb.B -- tri.B -- cycle, left_hatch + opacity(0.3));
