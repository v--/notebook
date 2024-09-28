usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/example_flow.asy' as graphs;

draw_example_flow_vertices();

draw_edge(v1, v2, L=Label('$e_1$', align=2NW), dash=true);
draw_edge(v1, v3, L=Label('$\widehat{e_2}$', align=2NE), bend=-0.1, dash=true);
draw_edge(v1, v3, L=Label('$e_2$', align=2SW), bend=0.1, is_arc=true, bold=true);
draw_edge(v2, v4, L=Label('$e_3$', align=2N), dash=true);
draw_edge(v3, v4, L=Label('$e_4$', align=2NW), is_arc=true, bold=true);
draw_edge(v3, v5, L=Label('$e_5$', align=2S), dash=true);
draw_edge(v4, v6, L=Label('$e_6$', align=2NE), bend=-0.1, is_arc=true, bold=true);
draw_edge(v5, v6, L=Label('$e_7$', align=2SE), dash=true);
draw_edge(v6, v4, L=Label('$\widehat{e_6}$', align=2SW), bend=0.1, dash=true);
draw_loop(v6, L=Label('$e_8$', align=E), dash=true);
