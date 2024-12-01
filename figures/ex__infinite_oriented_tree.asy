unitsize(1.5cm);

from notebook access grdraw;

label((-8, 0), '$\ldots$');
grdraw.edge((-7.9, 0), (-7, 0), is_arc=true);

grdraw.vert((-7, 0), L=Label('$n - 1$', align=2S));
grdraw.edge((-7, 0), (-6, 0), is_arc=true);

grdraw.vert((-6, 0), L=Label('$\phantom{1} n \phantom{1}$', align=2S));
grdraw.edge((-6, 0), (-5, 0), is_arc=true);

grdraw.vert((-5, 0), L=Label('$n + 1$', align=2S));
grdraw.edge((-5, 0), (-4.1, 0), is_arc=true);

label((-4, 0), '$\ldots$');
grdraw.edge((-3.9, 0), (-3, 0), is_arc=true);

grdraw.vert((-3, 0), L=Label('$-3$', align=2S));
grdraw.edge((-3, 0), (-2, 0), is_arc=true);

grdraw.vert((-2, 0), L=Label('$-2$', align=2S));
grdraw.edge((-2, 0), (-1, 0), is_arc=true);

grdraw.vert((-1, 0), L=Label('$-1$', align=2S));
grdraw.edge((-1, 0), (-0, 0), is_arc=true);

grdraw.vert((0, 0), L=Label('$0$', align=2S));
