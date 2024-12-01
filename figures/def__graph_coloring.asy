unitsize(1.5cm);

from notebook access grdraw, CompleteGraph, PetersenGraph;

PetersenGraph pg = PetersenGraph(5, 2);
pg.draw();

grdraw.vert(pg.outer[2], color=black);
grdraw.vert(pg.outer[4], color=black);
grdraw.vert(pg.inner[3], color=black);

grdraw.vert(pg.inner[0], color=mediumgray);
grdraw.vert(pg.inner[4], color=mediumgray);
grdraw.vert(pg.outer[1], color=mediumgray);

newpage();

CompleteGraph cg = CompleteGraph(6);

for (int i = 0; i <= 3; ++i)
  for (int j = 0; j < i; ++j)
    grdraw.edge(cg.vert[j], cg.vert[i]);

for (int i = 4; i < cg.n; ++i)
  for (int j = 0; j < i; ++j)
    grdraw.edge(cg.vert[j], cg.vert[i], color=mediumgray);

cg.draw_vertices();
