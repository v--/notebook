unitsize(1.5cm);

from notebook access grdraw, BipartiteGraph;

BipartiteGraph bg = BipartiteGraph(3, 3);
bg.draw_vertices();

for (int i = 0; i < 3; ++i) {
  grdraw.edge(bg.left[i], bg.right[i]);
  grdraw.edge(bg.right[i], bg.left[(i + 1) % 3]);
}
