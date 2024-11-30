usepackage('stix2');
unitsize(0.4cm);

import geometry;
import 'asymptote/geom/tri.asy' as tri;

triangle tri = triangleabc(5, 12, 13);

draw(tri);
draw_vertices(tri, draw_labels=false);
