unitsize(1.5cm);

from notebook access grdraw, TriangleGraph;

TriangleGraph tg = TriangleGraph();
tg.draw_vertices(b='$b$', c='$c$');
tg.draw_edge(oriented=true);

label(tg.a, '$a$', align=NW);
grdraw.loop(tg.a, angle=5 / 4 * pi, is_arc=true);
