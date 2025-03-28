unitsize(1.5cm);

from notebook access grdraw, BipartiteGraph;

BipartiteGraph bg = BipartiteGraph(2, 2);
bg.draw_vertices();

pair v5 = (1.5, 0.75);
grdraw.vert(v5);

grdraw.edge(bg.left[0], bg.right[0]);
grdraw.edge(bg.left[0], bg.right[1]);
grdraw.edge(bg.left[1], bg.right[1]);
grdraw.edge(bg.right[0], v5);
grdraw.edge(bg.left[1], v5, bend=0.2);
