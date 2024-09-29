usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/petersen.asy' as petersen_graph;

PetersenGraph(3, 1, outer_radius=1, inner_radius=1 / 3).draw();
