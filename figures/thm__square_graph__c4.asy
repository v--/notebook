usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/square.asy' as square_graph;

SquareGraph sg = SquareGraph();

sg.draw_vertices(a='$0$', b='$1$', c='$2$', d='$3$');
sg.draw_edges();
