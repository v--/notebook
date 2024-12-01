unitsize(1.5cm);

from notebook access grdraw, PetersenGraph;

PetersenGraph pg = PetersenGraph(5, 2);

for (int i = 0; i < pg.n; ++i) {
  grdraw.vert(pg.outer[i]);
  grdraw.vert(pg.inner[i]);
}

for (int i = 0; i < pg.n; ++i) {
  grdraw.edge(pg.outer[i], pg.inner[i % pg.n]);
  grdraw.edge(pg.inner[i], pg.inner[(i + pg.m) % pg.n]);
}

grdraw.edge(pg.outer[0], pg.outer[1], bold=true);
grdraw.edge(pg.outer[1], pg.outer[2], dash=true);
grdraw.edge(pg.outer[2], pg.outer[3], bold=true);
grdraw.edge(pg.outer[3], pg.outer[4], bold=true);
grdraw.edge(pg.outer[4], pg.outer[0], bold=true);

newpage();

for (int i = 0; i < pg.n; ++i) {
  grdraw.vert(pg.outer[i]);
  grdraw.vert(pg.inner[i]);
}

grdraw.edge(pg.outer[0], pg.outer[1]);
grdraw.edge(pg.outer[1], pg.outer[2], bold=true);
grdraw.edge(pg.outer[2], pg.outer[3], bold=true);
grdraw.edge(pg.outer[3], pg.outer[4]);
grdraw.edge(pg.outer[4], pg.outer[0]);

grdraw.edge(pg.outer[0], pg.inner[0]);
grdraw.edge(pg.outer[1], pg.inner[1], dash=true);
grdraw.edge(pg.outer[2], pg.inner[2]);
grdraw.edge(pg.outer[3], pg.inner[3], bold=true);
grdraw.edge(pg.outer[4], pg.inner[4]);

grdraw.edge(pg.inner[0], pg.inner[2]);
grdraw.edge(pg.inner[1], pg.inner[3], bold=true);
grdraw.edge(pg.inner[2], pg.inner[4]);
grdraw.edge(pg.inner[3], pg.inner[0]);
grdraw.edge(pg.inner[4], pg.inner[1]);

newpage();

for (int i = 0; i < pg.n; ++i) {
  grdraw.vert(pg.outer[i]);
  grdraw.vert(pg.inner[i]);
}

grdraw.edge(pg.outer[0], pg.outer[1]);
grdraw.edge(pg.outer[1], pg.outer[2], bold=true);
grdraw.edge(pg.outer[2], pg.outer[3], bold=true);
grdraw.edge(pg.outer[3], pg.outer[4]);
grdraw.edge(pg.outer[4], pg.outer[0]);

grdraw.edge(pg.outer[0], pg.inner[0]);
grdraw.edge(pg.outer[1], pg.inner[1], bold=true);
grdraw.edge(pg.outer[2], pg.inner[2]);
grdraw.edge(pg.outer[3], pg.inner[3], bold=true);
grdraw.edge(pg.outer[4], pg.inner[4]);

grdraw.edge(pg.inner[0], pg.inner[2]);
grdraw.edge(pg.inner[1], pg.inner[3], dash=true);
grdraw.edge(pg.inner[2], pg.inner[4]);
grdraw.edge(pg.inner[3], pg.inner[0]);
grdraw.edge(pg.inner[4], pg.inner[1]);
