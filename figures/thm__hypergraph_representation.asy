unitsize(1.5cm);

from notebook access grdraw;

pair v1 = (0, 0);
pair v2 = (1, 0.5);
pair v3 = (0, 1);
pair v4 = (1, 1.5);
pair v5 = (0, 2);

grdraw.vert(v1, L=Label('$v_1$', align=2W));
grdraw.vert(v2, L=Label('$v_2$', align=2E));
grdraw.vert(v3, L=Label('$v_3$', align=2W));
grdraw.vert(v4, L=Label('$v_4$', align=2E));
grdraw.vert(v5, L=Label('$v_5$', align=2W));

grdraw.edge(v1, v2, L=Label('$e_1$', align=2SE));
grdraw.edge(v2, v3, L=Label('$e_2$', align=2NE));
grdraw.hyperedge(new pair[] {v3, v4, v5}, L=Label('$e_3$'));

newpage();

pair v1 = (0, 2);
pair v2 = (0, 1.5);
pair v3 = (0, 1);
pair v4 = (0, 0.5);
pair v5 = (0, 0);

pair e1 = (1, 5/3);
pair e2 = (1, 3/3);
pair e3 = (1, 1/3);

grdraw.vert(v1, L=Label('$v_1$', align=2W));
grdraw.vert(v2, L=Label('$v_2$', align=2W));
grdraw.vert(v3, L=Label('$v_3$', align=2W));
grdraw.vert(v4, L=Label('$v_4$', align=2W));
grdraw.vert(v5, L=Label('$v_5$', align=2W));

grdraw.vert(e1, L=Label('$e_1$', align=2E));
grdraw.vert(e2, L=Label('$e_2$', align=2E));
grdraw.vert(e3, L=Label('$e_3$', align=2E));

grdraw.edge(v1, e1);
grdraw.edge(v2, e1);
grdraw.edge(v2, e2);
grdraw.edge(v3, e2);
grdraw.edge(v3, e3);
grdraw.edge(v4, e3);
grdraw.edge(v5, e3);
