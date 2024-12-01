unitsize(1.5cm);

from notebook access grdraw, CompleteGraph, PetersenGraph;

CompleteGraph cg = CompleteGraph(5);
cg.draw();

newpage();

cg.draw_vertices();

for (int i = 0; i < cg.n; ++i)
  for (int j = i + 1; j < cg.n; ++j)
    if (!(i == 1 && j == 2) && !(i == 0 && j == 4))
      grdraw.edge(cg.vert[i], cg.vert[j]);
