usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

pair a = (-1, -1);
pair b = (1, -1);
pair c = (0, 0);
pair d = (-1, 1);
pair e = (1, 1);

draw_vertex(a, L=Label('$a$', align=2W));
draw_vertex(b, L=Label('$b$', align=2E));
draw_vertex(c, L=Label('$c$', align=2W));
draw_vertex(d, L=Label('$d$', align=2W));
draw_vertex(e, L=Label('$e$', align=2E));

draw_edge(a, b, is_arc=true);
draw_edge(b, c, is_arc=true);
draw_edge(c, a, is_arc=true);

draw_edge(c, d, is_arc=true);
draw_edge(d, e, is_arc=true);
draw_edge(e, c, is_arc=true);
