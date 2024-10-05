usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

pair v1 = (0, 0);
pair v2 = (1, 0.5);
pair v3 = (0, 1);
pair v4 = (1, 1.5);
pair v5 = (0, 2);

draw_vertex(v1, L=Label('$v_1$', align=2W));
draw_vertex(v2, L=Label('$v_2$', align=2E));
draw_vertex(v3, L=Label('$v_3$', align=2W));
draw_vertex(v4, L=Label('$v_4$', align=2E));
draw_vertex(v5, L=Label('$v_5$', align=2W));

draw_edge(v1, v2, L=Label('$e_1$', align=2SE));
draw_edge(v2, v3, L=Label('$e_2$', align=2NE));
draw_hyperedge(new pair[] {v3, v4, v5}, L=Label('$e_3$'));

newpage();

pair v1 = (0, 2);
pair v2 = (0, 1.5);
pair v3 = (0, 1);
pair v4 = (0, 0.5);
pair v5 = (0, 0);

pair e1 = (1, 5/3);
pair e2 = (1, 3/3);
pair e3 = (1, 1/3);

draw_vertex(v1, L=Label('$v_1$', align=2W));
draw_vertex(v2, L=Label('$v_2$', align=2W));
draw_vertex(v3, L=Label('$v_3$', align=2W));
draw_vertex(v4, L=Label('$v_4$', align=2W));
draw_vertex(v5, L=Label('$v_5$', align=2W));

draw_vertex(e1, L=Label('$e_1$', align=2E));
draw_vertex(e2, L=Label('$e_2$', align=2E));
draw_vertex(e3, L=Label('$e_3$', align=2E));

draw_edge(v1, e1);
draw_edge(v2, e1);
draw_edge(v2, e2);
draw_edge(v3, e2);
draw_edge(v3, e3);
draw_edge(v4, e3);
draw_edge(v5, e3);
