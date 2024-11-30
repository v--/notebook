usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/square.asy' as square_graph;

SquareGraph sg = SquareGraph();

sg.draw_vertices(a='$00$', b='$10$', c='$11$', d='$01$');
sg.draw_edges();
