usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/complete.asy' as complete_graph;

CompleteGraph cg = CompleteGraph(5);

for (int i = 0; i < cg.n; ++i) {
  draw_edge(cg.vert[i], cg.vert[(i + 1) % cg.n]);

  for (int j = i + 2; j < cg.n; ++j) {
    draw_edge(cg.vert[i], cg.vert[j], color=mediumgray);
  }

  draw_vertex(cg.vert[i]);
}
