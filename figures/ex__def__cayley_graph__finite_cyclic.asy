unitsize(1.5cm);

from notebook access grdraw, lab, CycleGraph;

string vertex_label(int power) {
  if (power == 0) {
    return '$e$';
  }

  if (power == 1) {
    return '$a$';
  }

  return '$a^' + string(power) + '$';
}

pair o = (0, 0);
CycleGraph cg = CycleGraph(5);
int index_shift = ceil(cg.n / 2);

pair get_vertex(int power) {
  return cg.vert[(index_shift + power) % cg.n];
}

for (int i = 0; i < cg.n; ++i) {
  pair v = get_vertex(i);
  grdraw.vert(v, L=Label(vertex_label(i), align=2 * lab.align_oppose(v, o)));
  grdraw.edge(v, get_vertex(i + 1), is_arc=true);
}

newpage();

for (int i = 0; i < cg.n; ++i) {
  pair v = get_vertex(i);
  grdraw.vert(v, L=Label(vertex_label(i), align=2 * lab.align_oppose(v, o)));
  grdraw.edge(v, get_vertex(i + 1), bend=-0.1, is_arc=true);
  grdraw.edge(v, get_vertex(i - 1), bend=-0.1, is_arc=true);
}

newpage();

for (int i = 0; i < cg.n; ++i) {
  pair v = get_vertex(i);
  grdraw.vert(v, L=Label(vertex_label(i), align=2 * lab.align_oppose(v, o)));
  grdraw.edge(v, get_vertex(i + 1), is_arc=true);
  grdraw.edge(v, get_vertex(i + 2), is_arc=true);
}
