usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/bipartite.asy' as BipartiteGraph;

BipartiteGraph bg = BipartiteGraph(3, 3);
bg.draw_vertices();

for (int i = 0; i < 3; ++i) {
  draw_edge(bg.left[i], bg.right[i]);
  draw_edge(bg.right[i], bg.left[(i + 1) % 3]);
}
