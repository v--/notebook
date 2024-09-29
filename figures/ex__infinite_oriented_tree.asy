usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

label((-8, 0), '$\ldots$');
draw_edge((-7.9, 0), (-7, 0), is_arc=true);

draw_vertex((-7, 0), L=Label('$n - 1$', align=2S));
draw_edge((-7, 0), (-6, 0), is_arc=true);

draw_vertex((-6, 0), L=Label('$\phantom{1} n \phantom{1}$', align=2S));
draw_edge((-6, 0), (-5, 0), is_arc=true);

draw_vertex((-5, 0), L=Label('$n + 1$', align=2S));
draw_edge((-5, 0), (-4.1, 0), is_arc=true);

label((-4, 0), '$\ldots$');
draw_edge((-3.9, 0), (-3, 0), is_arc=true);

draw_vertex((-3, 0), L=Label('$-3$', align=2S));
draw_edge((-3, 0), (-2, 0), is_arc=true);

draw_vertex((-2, 0), L=Label('$-2$', align=2S));
draw_edge((-2, 0), (-1, 0), is_arc=true);

draw_vertex((-1, 0), L=Label('$-1$', align=2S));
draw_edge((-1, 0), (-0, 0), is_arc=true);

draw_vertex((0, 0), L=Label('$0$', align=2S));
