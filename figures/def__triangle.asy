usepackage('stix2');
unitsize(1cm);

import geometry;
import 'asymptote/geom/tri.asy' as tri;

triangle tri = triangleabc(3, 4, 5);

draw(tri);
draw_vertices(tri);
draw_angles(tri);
