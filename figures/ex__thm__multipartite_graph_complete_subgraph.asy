usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/square.asy' as square_graph;

SquareGraph sg = SquareGraph();

sg.draw_vertices();
sg.draw_edges();
draw_edge(sg.a, sg.c);
