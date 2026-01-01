access 'asymptote/graphs/grdraw.asy' as grdraw;
from 'asymptote/graphs/cycle.asy' access CycleGraph;

struct StarGraph {
  int n;
  pair center;
  pair[] vert;

  void operator init(int n, pair center = (0, 0), real radius = 0.75) {
    this.n = n;
    this.center = center;
    this.vert = CycleGraph(n, center, radius).vert;
  }

  void draw_vertices() {
    grdraw.vert(this.center);

    for (int i = 0; i < this.n; ++i)
      grdraw.vert(this.vert[i]);
  }

  void draw_edge() {
    for (int i = 0; i < this.n; ++i)
      grdraw.edge(this.center, this.vert[i]);
  }
}
