usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

label((-3, 0), '$\ldots$');
draw_edge((-2.9, 0), (-2, 0), is_arc=true);

draw_vertex((-2, 0), L=Label('$-2$', align=2S));
draw_edge((-2, 0), (-1, 0), is_arc=true);

draw_vertex((-1, 0), L=Label('$-1$', align=2S));
draw_edge((-1, 0), (0, 0), is_arc=true);

draw_vertex((0, 0), L=Label('$0$', align=2S));
draw_edge((0, 0), (1, 0), is_arc=true);

draw_vertex((1, 0), L=Label('$1$', align=2S));
draw_edge((1, 0), (2, 0), is_arc=true);

draw_vertex((2, 0), L=Label('$2$', align=2S));
draw_edge((2, 0), (2.9, 0), is_arc=true);

label((3, 0), '$\ldots$');
