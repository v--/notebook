usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/cycle.asy' as cycle_graph;
import 'asymptote/graphs.asy' as graphs;

pair O = (0, 0);
CycleGraph cg = CycleGraph(12);

cg.draw();
draw_vertex(O);

for (int i = 0; i < cg.vert.length; ++i) {
  draw_edge(O, cg.vert[i]);
}
