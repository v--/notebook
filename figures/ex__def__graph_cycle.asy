unitsize(1.5cm);

from notebook access grdraw;

pair a = (-1, -1);
pair b = (1, -1);
pair c = (0, 0);
pair d = (-1, 1);
pair e = (1, 1);

grdraw.vert(a, L=Label('$a$', align=2W));
grdraw.vert(b, L=Label('$b$', align=2E));
grdraw.vert(c, L=Label('$c$', align=2W));
grdraw.vert(d, L=Label('$d$', align=2W));
grdraw.vert(e, L=Label('$e$', align=2E));

grdraw.edge(a, b, is_arc=true);
grdraw.edge(b, c, is_arc=true);
grdraw.edge(c, a, is_arc=true);

grdraw.edge(c, d, is_arc=true);
grdraw.edge(d, e, is_arc=true);
grdraw.edge(e, c, is_arc=true);
