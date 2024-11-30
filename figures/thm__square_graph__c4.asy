usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/square.asy' as square_graph;

SquareGraph sg = SquareGraph();

sg.draw_vertices(a='$00 \mapsto 0$', b='$1 \mapsfrom 10$', c='$2 \mapsfrom 11$', d='$10 \mapsto 3$');
sg.draw_edges();
