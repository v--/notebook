unitsize(1.5cm);

from notebook access grdraw, CycleGraph;

CycleGraph cg = CycleGraph(3);

grdraw.vert(cg.vert[0], L=Label('$a$', align=2SW));
grdraw.vert(cg.vert[1], L=Label('$b$', align=2SE));
grdraw.vert(cg.vert[2], L=Label('$c$', align=2N));

grdraw.edge(cg.vert[0], cg.vert[1], is_arc=true);
grdraw.edge(cg.vert[0], cg.vert[2], is_arc=true);
grdraw.edge(cg.vert[1], cg.vert[2], is_arc=true);
