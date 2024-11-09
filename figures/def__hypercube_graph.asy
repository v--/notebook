usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

pair v000 = (0,   0);
pair v001 = (0,   4/3);
pair v010 = (4/3, 0);
pair v011 = (4/3, 4/3);
pair v100 = (2/3, 2/3);
pair v101 = (2/3, 2);
pair v110 = (2,   2/3);
pair v111 = (2,   2);

draw_vertex(v000, L=Label('000', align=2SW));
draw_vertex(v001, L=Label('001', align=2W));
draw_vertex(v010, L=Label('010', align=2S));
draw_vertex(v011, L=Label('011', align=2SE));
draw_vertex(v100, L=Label('100', align=2NE));
draw_vertex(v101, L=Label('101', align=2N));
draw_vertex(v110, L=Label('110', align=2E));
draw_vertex(v111, L=Label('111', align=2NE));

draw_edge(v000, v001);
draw_edge(v000, v010);
draw_edge(v000, v100, dash=true);
draw_edge(v001, v011);
draw_edge(v001, v101);
draw_edge(v010, v011);
draw_edge(v010, v110);
draw_edge(v100, v101, dash=true);
draw_edge(v100, v110, dash=true);
draw_edge(v011, v111);
draw_edge(v101, v111);
draw_edge(v110, v111);
