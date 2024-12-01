unitsize(1.5cm);

from notebook access grdraw;

pair g1 = (0, 0);
pair g2 = (1, 0.5);
pair g3 = (1, -0.5);

grdraw.vert(g1, L=Label('$\{ v_1, v_2, v_3, v_4 \}$', align=2W));
grdraw.vert(g2, L=Label('$\{ v_5 \}$', align=2NE));
grdraw.vert(g3, L=Label('$\{ v_6 \}$', align=2SE));

grdraw.edge(g1, g2, L=Label('$\{ e_5 \}$', align=3N), is_arc=true);
grdraw.edge(g1, g3, L=Label('$\{ e_6 \}$', align=3S), is_arc=true);
grdraw.edge(g2, g3, L=Label('$\{ e_7 \}$', align=2E), is_arc=true);
