usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;

pair A = (0, 0);
pair B = (0, 1);
pair C = (0, -1);
pair D = (2, 0);

draw_vertex(A, L=Label('$A$', align=2W));
draw_vertex(B, L=Label('$B$', align=2W));
draw_vertex(C, L=Label('$C$', align=2W));
draw_vertex(D, L=Label('$D$', align=2E));

draw_edge(A, B, L=Label('$a$', align=2W), bend=-0.15);
draw_edge(A, B, L=Label('$b$', align=2E), bend=0.15);
draw_edge(A, C, L=Label('$c$', align=2W), bend=-0.15);
draw_edge(A, C, L=Label('$d$', align=2E), bend=0.15);
draw_edge(A, D, L=Label('$e$', align=2N));
draw_edge(B, D, L=Label('$f$', align=2NE), bend=-0.1, bend_at=0.6);
draw_edge(C, D, L=Label('$g$', align=2SE), bend=0.1, bend_at=0.6);
