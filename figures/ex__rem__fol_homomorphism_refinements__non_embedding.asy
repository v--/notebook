unitsize(1.5cm);

from notebook access grdraw, CycleGraph;

CycleGraph g1 = CycleGraph(3, center=(-1, 0), radius=0.75);
g1.draw_vertices();

grdraw.edge(g1.vert[1], g1.vert[2], is_arc=true);
grdraw.edge(g1.vert[0], g1.vert[2], is_arc=true);

pair g21 = (1, g1.vert[1].y);
pair g22 = (1, g1.vert[2].y);

grdraw.vert(g21);
grdraw.vert(g22);
grdraw.edge(g21, g22, is_arc=true);

grdraw.edge(g1.vert[0], g21, bend=-0.2, dash=true, is_arc=true);
grdraw.edge(g1.vert[1], g21, bend=0.05, dash=true, is_arc=true);
grdraw.edge(g1.vert[2], g22, bend=0.2, dash=true, is_arc=true);
