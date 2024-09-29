usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/cycle.asy' as cycle_graph;

CycleGraph cg = CycleGraph(3);

draw_vertex(cg.vert[0], L=Label('$a$', align=2SW));
draw_vertex(cg.vert[1], L=Label('$b$', align=2SE));
draw_vertex(cg.vert[2], L=Label('$c$', align=2N));

draw_edge(cg.vert[0], cg.vert[1], is_arc=true);
draw_edge(cg.vert[0], cg.vert[2], is_arc=true);
draw_edge(cg.vert[1], cg.vert[2], is_arc=true);
