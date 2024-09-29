usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/star.asy' as StarGraph;

StarGraph sg = StarGraph(5);
sg.draw_vertices();
sg.draw_edges();
