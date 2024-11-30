usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/cube.asy' as cube;

CubeGraph cg = CubeGraph(segments=1);
cg.draw_vertices();
cg.draw_edges();
