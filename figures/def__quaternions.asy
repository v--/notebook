usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/triangle.asy' as triangle_graph;

TriangleGraph tg = TriangleGraph();
tg.draw_vertices(c='$i$', a='$j$', b='$k$');
tg.draw_edges(oriented=true);
