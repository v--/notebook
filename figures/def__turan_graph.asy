usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/petersen.asy' as petersen_graph;
import 'asymptote/graphs/complete.asy' as complete_graph;

CompleteGraph cg = CompleteGraph(5);
cg.draw();

newpage();

cg.draw_vertices();

for (int i = 0; i < cg.n; ++i)
  for (int j = i + 1; j < cg.n; ++j)
    if (!(i == 1 && j == 2) && !(i == 0 && j == 4))
      draw_edge(cg.vert[i], cg.vert[j]);
