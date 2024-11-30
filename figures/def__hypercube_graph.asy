usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/cube.asy' as cube;

CubeGraph cg = CubeGraph(segments=1, dist=2);
cg.draw_vertices();
cg.draw_edges();

label(cg.vertices[0][0][0], '000', align=2SW);
label(cg.vertices[1][0][0], '100', align=2S);

label(cg.vertices[0][1][0], '010', align=2W);
label(cg.vertices[1][1][0], '110', align=2SE);

label(cg.vertices[0][0][1], '001', align=2NW);
label(cg.vertices[1][0][1], '101', align=2SE);

label(cg.vertices[0][1][1], '011', align=2NW);
label(cg.vertices[1][1][1], '111', align=2NE);
