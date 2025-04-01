unitsize(1cm);

import geometry;

from notebook access geom;

triangle tri = triangleabc(3, 4, 4.5);

draw(tri);
geom.draw_vertices(tri);
geom.mark_angles(tri);

triangle inner_tri = triangle(midpoint(tri.BC), midpoint(tri.AC), midpoint(tri.AB));

draw(inner_tri);
geom.draw_vertices(inner_tri, a='$M_A$', b='$M_B$', c='$M_C$');
geom.mark_angles(inner_tri);
geom.mark_angle(
  tri.A, inner_tri.B, inner_tri.C,
  L=Label('$\\gamma$')
);

geom.mark_angle(
  inner_tri.A, inner_tri.B, tri.C,
  L=Label('$\\alpha$')
);
