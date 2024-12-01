unitsize(1.5cm);

from notebook access grdraw, SquareGraph;

SquareGraph sg = SquareGraph(dist=1);

sg.draw_vertices(a='$a$', b='$b$', c='$d$', d='$c$');
sg.draw_edge(ab='$3$', ad='$2$', dc='$1$', bc='$1$', oriented=true);
grdraw.edge(sg.a, sg.c, L=Label('$4$', align=NW), is_arc=true);
