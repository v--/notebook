unitsize(1.5cm);

from notebook access grdraw, lab, PetersenGraph;

PetersenGraph pg = PetersenGraph(3, 1, outer_radius=1.5, inner_radius=0.5);

grdraw.vert(pg.inner[0], L=Label('$e$', align=1.2S));
grdraw.vert(pg.inner[1], L=Label('$a$', align=1.2S));
grdraw.vert(pg.inner[2], L=Label('$a^2$', align=1NW));

grdraw.vert(pg.outer[0], L=Label('$b$', align=1.5W));
grdraw.vert(pg.outer[1], L=Label('$ab = ba$', align=1.5E));
grdraw.vert(pg.outer[2], L=Label('$a^2b = aba$', align=1.5W));

for (int i = 0; i < pg.n; ++i) {
  grdraw.edge(pg.outer[i], pg.outer[(i + 1) % pg.n], is_arc=true);
  grdraw.edge(pg.inner[i], pg.outer[i % pg.n], is_arc=true, dash=true);
  grdraw.edge(pg.inner[i], pg.inner[(i + pg.m) % pg.n], is_arc=true);
}
