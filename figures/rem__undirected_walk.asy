usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

pair a = (0, -1);
pair b = (-1, 0);
pair c = (1, 0);
pair d = (0, 1);

void draw_vertices() {
  draw_vertex(a, L=Label('$a$', align=2S));
  draw_vertex(b, L=Label('$b$', align=2W));
  draw_vertex(c, L=Label('$c$', align=2E));
  draw_vertex(d, L=Label('$d$', align=2N));
}

draw_vertices();

draw_edge(a, b, is_arc=true);
draw_edge(b, c, is_arc=true);
draw_edge(c, a, is_arc=true);
draw_edge(c, d, is_arc=true);
draw_edge(d, b, is_arc=true);

newpage();

draw_vertices();

draw_edge(a, b, is_arc=true, bold=true);
draw_edge(b, c, is_arc=true, bold=true);
draw_edge(c, a, is_arc=true, dash=true);
draw_edge(c, d, is_arc=true, dash=true);
draw_edge(d, b, is_arc=true, dash=true);

newpage();

draw_vertices();

draw_edge(a, b, is_arc=true, bold=true);
draw_edge(b, c, is_arc=true, bold=true);
draw_edge(c, a, dash=true);
draw_edge(c, d, dash=true);
draw_edge(d, b, dash=true);

newpage();

draw_vertices();

draw_edge(a, b, is_arc=true, bold=true);
draw_edge(a, c, bend=0.15, is_arc=true, dash=true);
draw_edge(b, a, bend=0.15, is_arc=true, dash=true);
draw_edge(b, c, bend=-0.15, is_arc=true, bold=true);
draw_edge(b, d, bend=-0.15, is_arc=true, dash=true);
draw_edge(c, a, is_arc=true, dash=true);
draw_edge(c, b, bend=0.15, is_arc=true, dash=true);
draw_edge(c, d, is_arc=true, dash=true);
draw_edge(d, b, is_arc=true, dash=true);
draw_edge(d, c, bend=-0.15, is_arc=true, dash=true);

newpage();

draw_vertices();

draw_edge(a, b, is_arc=true, dash=true);
draw_edge(a, c, bend=0.15, is_arc=true, dash=true);
draw_edge(b, a, bend=0.15, is_arc=true, bold=true);
draw_edge(b, c, bend=-0.15, is_arc=true, dash=true);
draw_edge(b, d, bend=-0.15, is_arc=true, dash=true);
draw_edge(c, a, is_arc=true, dash=true);
draw_edge(c, b, bend=0.15, is_arc=true, bold=true);
draw_edge(c, d, is_arc=true, dash=true);
draw_edge(d, b, is_arc=true, dash=true);
draw_edge(d, c, bend=-0.15, is_arc=true, dash=true);
