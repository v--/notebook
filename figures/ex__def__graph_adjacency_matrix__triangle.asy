usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/triangle.asy' as triangle_graph;

TriangleGraph tg = TriangleGraph();
tg.draw_vertices(b='$b$', c='$c$');
tg.draw_edges(oriented=true);

label(tg.a, '$a$', align=NW);
draw_loop(tg.a, angle=5 / 4 * pi, is_arc=true);
