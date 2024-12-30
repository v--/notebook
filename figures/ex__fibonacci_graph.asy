unitsize(1.5cm);

from notebook access grdraw;

pair u = (0, 0);
pair v = (0, -0.7);

grdraw.vert(u, L=Label('$u$', align=2N));
grdraw.vert(v, L=Label('$v$', align=2S));
grdraw.edge(u, v, bend=0.1, is_arc=true);
grdraw.edge(v, u, bend=-0.1, is_arc=true);
grdraw.loop(v, is_arc=true);
