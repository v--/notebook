unitsize(1.5cm);

from notebook access grdraw, CompleteGraph, PetersenGraph;

PetersenGraph pg = PetersenGraph(5, 2);
pg.draw();

grdraw.vert(pg.outer[2], p=black);
grdraw.vert(pg.outer[4], p=black);
grdraw.vert(pg.inner[3], p=black);

grdraw.vert(pg.inner[0], p=mediumgray);
grdraw.vert(pg.inner[4], p=mediumgray);
grdraw.vert(pg.outer[1], p=mediumgray);

newpage();

CompleteGraph cg = CompleteGraph(6);

for (int i = 0; i <= 3; ++i)
  for (int j = 0; j < i; ++j)
    grdraw.edge(cg.vert[j], cg.vert[i]);

for (int i = 4; i < cg.n; ++i)
  for (int j = 0; j < i; ++j)
    grdraw.edge(cg.vert[j], cg.vert[i], p=mediumgray);

cg.draw_vertices();
