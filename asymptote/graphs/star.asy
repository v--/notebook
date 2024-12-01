access 'asymptote/graphs/grdraw.asy' as grdraw;
from 'asymptote/graphs/cycle.asy' access CycleGraph;

struct StarGraph {
  int n;
  pair origin;
  pair[] vert;

  void operator init(int n, pair origin = (0, 0), real radius = 0.75) {
    this.n = n;
    this.origin = origin;
    this.vert = CycleGraph(n, radius).vert;
  }

  void draw_vertices() {
    grdraw.vert(this.origin);

    for (int i = 0; i < this.n; ++i)
      grdraw.vert(this.vert[i]);
  }

  void draw_edge() {
    for (int i = 0; i < this.n; ++i)
      grdraw.edge(this.origin, this.vert[i]);
  }
}
