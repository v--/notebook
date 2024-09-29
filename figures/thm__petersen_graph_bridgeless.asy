usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/petersen.asy' as petersen_graph;

PetersenGraph pg = PetersenGraph(5, 2);

for (int i = 0; i < pg.n; ++i) {
  draw_vertex(pg.outer[i]);
  draw_vertex(pg.inner[i]);
}

for (int i = 0; i < pg.n; ++i) {
  draw_edge(pg.outer[i], pg.inner[i % pg.n]);
  draw_edge(pg.inner[i], pg.inner[(i + pg.m) % pg.n]);
}

draw_edge(pg.outer[0], pg.outer[1], bold=true);
draw_edge(pg.outer[1], pg.outer[2], dash=true);
draw_edge(pg.outer[2], pg.outer[3], bold=true);
draw_edge(pg.outer[3], pg.outer[4], bold=true);
draw_edge(pg.outer[4], pg.outer[0], bold=true);

newpage();

for (int i = 0; i < pg.n; ++i) {
  draw_vertex(pg.outer[i]);
  draw_vertex(pg.inner[i]);
}

draw_edge(pg.outer[0], pg.outer[1]);
draw_edge(pg.outer[1], pg.outer[2], bold=true);
draw_edge(pg.outer[2], pg.outer[3], bold=true);
draw_edge(pg.outer[3], pg.outer[4]);
draw_edge(pg.outer[4], pg.outer[0]);

draw_edge(pg.outer[0], pg.inner[0]);
draw_edge(pg.outer[1], pg.inner[1], dash=true);
draw_edge(pg.outer[2], pg.inner[2]);
draw_edge(pg.outer[3], pg.inner[3], bold=true);
draw_edge(pg.outer[4], pg.inner[4]);

draw_edge(pg.inner[0], pg.inner[2]);
draw_edge(pg.inner[1], pg.inner[3], bold=true);
draw_edge(pg.inner[2], pg.inner[4]);
draw_edge(pg.inner[3], pg.inner[0]);
draw_edge(pg.inner[4], pg.inner[1]);

newpage();

for (int i = 0; i < pg.n; ++i) {
  draw_vertex(pg.outer[i]);
  draw_vertex(pg.inner[i]);
}

draw_edge(pg.outer[0], pg.outer[1]);
draw_edge(pg.outer[1], pg.outer[2], bold=true);
draw_edge(pg.outer[2], pg.outer[3], bold=true);
draw_edge(pg.outer[3], pg.outer[4]);
draw_edge(pg.outer[4], pg.outer[0]);

draw_edge(pg.outer[0], pg.inner[0]);
draw_edge(pg.outer[1], pg.inner[1], bold=true);
draw_edge(pg.outer[2], pg.inner[2]);
draw_edge(pg.outer[3], pg.inner[3], bold=true);
draw_edge(pg.outer[4], pg.inner[4]);

draw_edge(pg.inner[0], pg.inner[2]);
draw_edge(pg.inner[1], pg.inner[3], dash=true);
draw_edge(pg.inner[2], pg.inner[4]);
draw_edge(pg.inner[3], pg.inner[0]);
draw_edge(pg.inner[4], pg.inner[1]);
