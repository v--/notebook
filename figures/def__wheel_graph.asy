unitsize(1.5cm);

from notebook access grdraw, CycleGraph;

pair O = (0, 0);
CycleGraph cg = CycleGraph(12);

cg.draw();
grdraw.vert(O);

for (int i = 0; i < cg.vert.length; ++i) {
  grdraw.edge(O, cg.vert[i]);
}
