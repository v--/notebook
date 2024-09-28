import 'asymptote/graphs.asy' as graphs;

pair v1 = (0, 0);
pair v2 = (1, 1);
pair v3 = (1, -1);
pair v4 = (3, 1);
pair v5 = (3, -1);
pair v6 = (4, 0);

void draw_example_flow_vertices() {
  draw_vertex(v1, L=Label('$v_1$', align=2W));
  draw_vertex(v2, L=Label('$v_2$', align=2N));
  draw_vertex(v3, L=Label('$v_3$', align=2S));
  draw_vertex(v4, L=Label('$v_4$', align=2N));
  draw_vertex(v5, L=Label('$v_5$', align=2S));
  draw_vertex(v6, L=Label('$v_6$', align=2S));
}
