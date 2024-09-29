usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/cycle.asy' as cycle_graph;

int[] points = new int[] { 0, 7, 12, 1, 6, 13 };

CycleGraph cg = CycleGraph(18);

for (int i = 0; i < points.length; ++i) {
  draw_vertex(cg.vert[points[i]]);
  draw_edge(
    cg.vert[points[i]],
    cg.vert[points[(i + 1) % points.length]]
  );
}
