unitsize(1.5cm);

from notebook access grdraw, CycleGraph;

CycleGraph cg = CycleGraph(6);

for (int i = 0; i < cg.n; ++i)
  grdraw.vert(cg.vert[i], L=Label('$' + string(i + 1) + '$', align=2 * cg.vert[i]));

for (int i = 0; i < cg.n; i += 2)
  grdraw.edge(cg.vert[i], cg.vert[(i + 2) % cg.n], dash=true, is_arc=true);

for (int i = 1; i < cg.n; i += 2)
  grdraw.edge(cg.vert[i], cg.vert[(i + 2) % cg.n], is_arc=true);
