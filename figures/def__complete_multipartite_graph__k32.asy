usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/star.asy' as StarGraph;

BipartiteGraph bg = BipartiteGraph(3, 2, xdist=1);
bg.draw_vertices();
bg.draw_edges_complete();
