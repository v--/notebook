usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/bipartite.asy' as BipartiteGraph;

BipartiteGraph bg = BipartiteGraph(2, 2);
bg.draw_vertices();
bg.draw_edges_complete();

draw_vertex(bg.left[0], L=Label('$0 \mapsto \iota_1(0)$', align=2W));
draw_vertex(bg.left[1], L=Label('$2 \mapsto \iota_1(1)$', align=2W));

draw_vertex(bg.right[0], L=Label('$\iota_2(0) \mapsfrom 1$', align=2E));
draw_vertex(bg.right[1], L=Label('$\iota_2(1) \mapsfrom 3$', align=2E));
