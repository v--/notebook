unitsize(1.5cm);

from notebook access grdraw, CycleGraph;

CycleGraph cg = CycleGraph(6);

pair u = (-2, sin(5pi / 3));
pair v = (2, sin(5pi / 3));

grdraw.vert(u, L=Label('$u$', align=2S));
grdraw.vert(v, L=Label('$v$', align=2S));

for (int i = 0; i < cg.n; ++i) {
  grdraw.vert(cg.vert[i], L=Label('$v_' + string((i + 1) % 6) + '$', align=2 * cg.vert[i]));
}

grdraw.edge(u, cg.vert[0], L=Label('$f_1$', align=2S));
grdraw.edge(cg.vert[0], cg.vert[1], L=Label('$e_2$', align=2S), dash=true);
grdraw.edge(cg.vert[1], cg.vert[2], L=Label('$e_3$', align=2SE));
grdraw.edge(cg.vert[2], cg.vert[3], L=Label('$e_4$', align=2NE));
grdraw.edge(cg.vert[3], cg.vert[4], L=Label('$e_5$', align=2N));
grdraw.edge(cg.vert[4], cg.vert[5], L=Label('$e_6$', align=2NW));
grdraw.edge(cg.vert[5], cg.vert[0], L=Label('$e_1$', align=2SW));
grdraw.edge(v, cg.vert[1], L=Label('$f_2$', align=2S));
