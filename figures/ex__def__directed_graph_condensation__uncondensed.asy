unitsize(1.5cm);

from notebook access grdraw, ExampleFlowGraph;

ExampleFlowGraph fg = ExampleFlowGraph();
fg.draw_vertices(shift_v6=false);

grdraw.edge(fg.v1, fg.v2, L=Label('$e_1$', align=2NW), is_arc=true);
grdraw.edge(fg.v1, fg.v3, L=Label('$e_2$', align=2SW), is_arc=true);
grdraw.edge(fg.v2, fg.v4, L=Label('$e_3$', align=2N), is_arc=true);
grdraw.edge(fg.v3, fg.v4, L=Label('$e_4$', align=2NW), is_arc=true);
grdraw.edge(fg.v3, fg.v5, L=Label('$e_5$', align=2S), is_arc=true);
grdraw.edge(fg.v4, fg.v6, L=Label('$e_6$', align=2NE), is_arc=true);
grdraw.edge(fg.v5, fg.v6, L=Label('$e_7$', align=2SE), is_arc=true);
grdraw.edge(fg.v3, fg.v2, L=Label('$e_8$', align=2E), is_arc=true, bold=true);
grdraw.edge(fg.v4, fg.v1, L=Label('$e_9$', align=2NE), bend=-0.8, bend_at=0.1, is_arc=true, bold=true);
