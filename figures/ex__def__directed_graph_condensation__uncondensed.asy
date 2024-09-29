usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/example_flow.asy' as example_flow_graph;

ExampleFlowGraph fg = ExampleFlowGraph();
fg.draw_vertices(shift_v6=false);

draw_edge(fg.v1, fg.v2, L=Label('$e_1$', align=2NW), is_arc=true);
draw_edge(fg.v1, fg.v3, L=Label('$e_2$', align=2SW), is_arc=true);
draw_edge(fg.v2, fg.v4, L=Label('$e_3$', align=2N), is_arc=true);
draw_edge(fg.v3, fg.v4, L=Label('$e_4$', align=2NW), is_arc=true);
draw_edge(fg.v3, fg.v5, L=Label('$e_5$', align=2S), is_arc=true);
draw_edge(fg.v4, fg.v6, L=Label('$e_6$', align=2NE), is_arc=true);
draw_edge(fg.v5, fg.v6, L=Label('$e_7$', align=2SE), is_arc=true);
draw_edge(fg.v3, fg.v2, L=Label('$e_8$', align=2E), is_arc=true, bold=true);
draw_edge(fg.v4, fg.v1, L=Label('$e_9$', align=2NE), bend=-0.9, bend_at=0.2, is_arc=true, bold=true);
