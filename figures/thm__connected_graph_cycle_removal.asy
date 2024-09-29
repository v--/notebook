usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs/cycle.asy' as cycle_graph;

CycleGraph cg = CycleGraph(6);

pair u = (-2, sin(5pi / 3));
pair v = (2, sin(5pi / 3));

draw_vertex(u, L=Label('$u$', align=2S));
draw_vertex(v, L=Label('$v$', align=2S));

for (int i = 0; i < cg.n; ++i) {
  draw_vertex(cg.vert[i], L=Label('$v_' + string((i + 1) % 6) + '$', align=2 * cg.vert[i]));
}

draw_edge(u, cg.vert[0], L=Label('$f_1$', align=2S));
draw_edge(cg.vert[0], cg.vert[1], L=Label('$e_2$', align=2S), dash=true);
draw_edge(cg.vert[1], cg.vert[2], L=Label('$e_3$', align=2SE));
draw_edge(cg.vert[2], cg.vert[3], L=Label('$e_4$', align=2NE));
draw_edge(cg.vert[3], cg.vert[4], L=Label('$e_5$', align=2N));
draw_edge(cg.vert[4], cg.vert[5], L=Label('$e_6$', align=2NW));
draw_edge(cg.vert[5], cg.vert[0], L=Label('$e_1$', align=2SW));
draw_edge(v, cg.vert[1], L=Label('$f_2$', align=2S));
