usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/square.asy' as square_graph;

SquareGraph sg = SquareGraph(dist=1);

sg.draw_vertices(a='$a$', b='$b$', c='$d$', d='$c$');
sg.draw_edges(ab='$3$', ad='$2$', dc='$1$', bc='$1$', oriented=true);
draw_edge(sg.a, sg.c, L=Label('$4$', align=NW), is_arc=true);
