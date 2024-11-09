usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/square.asy' as square_graph;

SquareGraph sg = SquareGraph();

sg.draw_vertices(a='$00$', b='$01$', c='$11$', d='$10$');
sg.draw_edges();
