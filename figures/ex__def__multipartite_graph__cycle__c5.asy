usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/bipartite.asy' as BipartiteGraph;

BipartiteGraph bg = BipartiteGraph(2, 2);
bg.draw_vertices();

pair v5 = (1.5, 0.75);
draw_vertex(v5);

draw_edge(bg.left[0], bg.right[0]);
draw_edge(bg.left[0], bg.right[1]);
draw_edge(bg.left[1], bg.right[1]);
draw_edge(bg.right[0], v5);
draw_edge(bg.left[1], v5, bend=-0.3);
