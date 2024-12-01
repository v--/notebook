unitsize(1.5cm);

from notebook access TriangleGraph;

TriangleGraph tg = TriangleGraph();
tg.draw_vertices(c='$i$', a='$j$', b='$k$');
tg.draw_edge(oriented=true);
