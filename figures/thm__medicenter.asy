usepackage('stix2');
unitsize(1cm);

import geometry;
import 'asymptote/labels.asy' as labels;
import 'asymptote/geom/tri.asy' as tri;
import 'asymptote/geom/segment.asy' as segment;

triangle tri = triangleabc(3, 4, 5);

segment ma = median(tri.VA);
segment mb = median(tri.VB);
segment mc = median(tri.VC);

point M = intersectionpoint(mc, mb);

draw(tri);
draw_segment(ma, LA='$A$', LB='$M_A$');
draw_segment(mb, LA='$B$', LB='$M_B$');
draw_segment(mc, LA='$C$', LB='$M_C$');

dot(M, L=Label('$M$', align=rotate(50) * 2E));
