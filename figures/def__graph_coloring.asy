usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/petersen.asy' as petersen_graph;
import 'asymptote/graphs/complete.asy' as complete_graph;

PetersenGraph pg = PetersenGraph(5, 2);
pg.draw();

draw_vertex(pg.outer[2], color=black);
draw_vertex(pg.outer[4], color=black);
draw_vertex(pg.inner[3], color=black);

draw_vertex(pg.inner[0], color=mediumgray);
draw_vertex(pg.inner[4], color=mediumgray);
draw_vertex(pg.outer[1], color=mediumgray);

newpage();

CompleteGraph cg = CompleteGraph(6);

for (int i = 0; i <= 3; ++i)
  for (int j = 0; j < i; ++j)
    draw_edge(cg.vert[j], cg.vert[i]);

for (int i = 4; i < cg.n; ++i)
  for (int j = 0; j < i; ++j)
    draw_edge(cg.vert[j], cg.vert[i], color=mediumgray);

cg.draw_vertices();
