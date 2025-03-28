unitsize(1.5cm);

from notebook access grdraw;

pair a = (0, -1);
pair b = (-1, 0);
pair c = (1, 0);
pair d = (0, 1);

void draw_vertices() {
  grdraw.vert(a, L=Label('$a$', align=2S));
  grdraw.vert(b, L=Label('$b$', align=2W));
  grdraw.vert(c, L=Label('$c$', align=2E));
  grdraw.vert(d, L=Label('$d$', align=2N));
}

draw_vertices();

grdraw.edge(a, b, is_arc=true);
grdraw.edge(b, c, is_arc=true);
grdraw.edge(c, a, is_arc=true);
grdraw.edge(c, d, is_arc=true);
grdraw.edge(d, b, is_arc=true);

newpage();

draw_vertices();

grdraw.edge(a, b, is_arc=true, bold=true);
grdraw.edge(b, c, is_arc=true, bold=true);
grdraw.edge(c, a, is_arc=true, dash=true);
grdraw.edge(c, d, is_arc=true, dash=true);
grdraw.edge(d, b, is_arc=true, dash=true);

newpage();

draw_vertices();

grdraw.edge(a, b, is_arc=true, bold=true);
grdraw.edge(b, c, is_arc=true, bold=true);
grdraw.edge(c, a, dash=true);
grdraw.edge(c, d, dash=true);
grdraw.edge(d, b, dash=true);

newpage();

draw_vertices();

grdraw.edge(a, b, is_arc=true, bold=true);
grdraw.edge(a, c, bend=-0.2, is_arc=true, dash=true);
grdraw.edge(b, a, bend=-0.2, is_arc=true, dash=true);
grdraw.edge(b, c, bend=0.2, is_arc=true, bold=true);
grdraw.edge(b, d, bend=0.2, is_arc=true, dash=true);
grdraw.edge(c, a, is_arc=true, dash=true);
grdraw.edge(c, b, bend=-0.2, is_arc=true, dash=true);
grdraw.edge(c, d, is_arc=true, dash=true);
grdraw.edge(d, b, is_arc=true, dash=true);
grdraw.edge(d, c, bend=0.2, is_arc=true, dash=true);

newpage();

draw_vertices();

grdraw.edge(a, b, is_arc=true, dash=true);
grdraw.edge(a, c, bend=-0.2, is_arc=true, dash=true);
grdraw.edge(b, a, bend=-0.2, is_arc=true, bold=true);
grdraw.edge(b, c, bend=0.2, is_arc=true, dash=true);
grdraw.edge(b, d, bend=0.2, is_arc=true, dash=true);
grdraw.edge(c, a, is_arc=true, dash=true);
grdraw.edge(c, b, bend=-0.2, is_arc=true, bold=true);
grdraw.edge(c, d, is_arc=true, dash=true);
grdraw.edge(d, b, is_arc=true, dash=true);
grdraw.edge(d, c, bend=0.2, is_arc=true, dash=true);
