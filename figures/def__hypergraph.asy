usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/example_flow.asy' as example_flow_graph;

ExampleFlowGraph fg = ExampleFlowGraph();
fg.draw_vertices(shift_v6=true);

draw_edge(fg.v1, fg.v2, L=Label('$e_1$', align=2NW));
draw_edge(fg.v1, fg.v3, L=Label('$\widehat{e_2}$', align=2NE), bend=-0.1, dash=true);
draw_edge(fg.v1, fg.v3, L=Label('$e_2$', align=2SW), bend=0.1);
draw_edge(fg.v2, fg.v4, L=Label('$e_3$', align=2N));
draw_edge(fg.v3, fg.v4, L=Label('$e_4$', align=2NW));
draw_edge(fg.v3, fg.v5, L=Label('$e_5$', align=2S));
draw_edge(fg.v4, fg.v6, L=Label('$e_6$', align=2NE), bend=-0.1);
draw_edge(fg.v5, fg.v6, L=Label('$e_7$', align=2SE));
draw_edge(fg.v6, fg.v4, L=Label('$\widehat{e_6}$', align=2SW), bend=0.1, dash=true);
draw_loop(fg.v6, L=Label('$e_8$', align=E), dash=true);
draw_hyperedge(new pair[] {fg.v3, fg.v4, fg.v5}, L=Label('$e_9$'));
