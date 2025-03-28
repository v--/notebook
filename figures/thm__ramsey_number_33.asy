unitsize(1.5cm);

from notebook access grdraw, CompleteGraph;

CompleteGraph cg = CompleteGraph(5);

for (int i = 0; i < cg.n; ++i) {
  grdraw.edge(cg.vert[i], cg.vert[(i + 1) % cg.n]);

  for (int j = i + 2; j < cg.n; ++j) {
    grdraw.edge(cg.vert[i], cg.vert[j], p=mediumgray);
  }

  grdraw.vert(cg.vert[i]);
}
