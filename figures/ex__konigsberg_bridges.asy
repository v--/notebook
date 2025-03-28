unitsize(1.5cm);

from notebook access grdraw;

pair A = (0, 0);
pair B = (0, 1);
pair C = (0, -1);
pair D = (2, 0);

grdraw.vert(A, L=Label('$A$', align=2W));
grdraw.vert(B, L=Label('$B$', align=2W));
grdraw.vert(C, L=Label('$C$', align=2W));
grdraw.vert(D, L=Label('$D$', align=2E));

grdraw.edge(A, B, L=Label('$a$', align=W), bend=0.15);
grdraw.edge(A, B, L=Label('$b$', align=E), bend=-0.15);
grdraw.edge(A, C, L=Label('$c$', align=W), bend=-0.15);
grdraw.edge(A, C, L=Label('$d$', align=E), bend=0.15);
grdraw.edge(A, D, L=Label('$e$', align=N));
grdraw.edge(B, D, L=Label('$f$', align=NE), bend=0.1, bend_at=0.7);
grdraw.edge(C, D, L=Label('$g$', align=SE), bend=-0.1, bend_at=0.7);
