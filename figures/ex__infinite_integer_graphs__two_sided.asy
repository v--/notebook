unitsize(1.5cm);

from notebook access grdraw;

label((-3, 0), '$\ldots$');
grdraw.edge((-2.9, 0), (-2, 0), is_arc=true);

grdraw.vert((-2, 0), L=Label('$-2$', align=2S));
grdraw.edge((-2, 0), (-1, 0), is_arc=true);

grdraw.vert((-1, 0), L=Label('$-1$', align=2S));
grdraw.edge((-1, 0), (0, 0), is_arc=true);

grdraw.vert((0, 0), L=Label('$0$', align=2S));
grdraw.edge((0, 0), (1, 0), is_arc=true);

grdraw.vert((1, 0), L=Label('$1$', align=2S));
grdraw.edge((1, 0), (2, 0), is_arc=true);

grdraw.vert((2, 0), L=Label('$2$', align=2S));
grdraw.edge((2, 0), (2.9, 0), is_arc=true);

label((3, 0), '$\ldots$');
