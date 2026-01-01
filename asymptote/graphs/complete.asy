access 'asymptote/graphs/grdraw.asy' as grdraw;
from 'asymptote/graphs/cycle.asy' access CycleGraph;

struct CompleteGraph {
  int n;
  pair[] vert;

  void operator init(int n, pair center = (0, 0), real radius = 0.75) {
    this.n = n;

    if (n == 4) {
      this.vert = CycleGraph(3, center, radius).vert;
      this.vert[3] = center;
    } else {
      this.vert = CycleGraph(n, center, radius).vert;
    }
  }

  void draw_vertices() {
    for (int i = 0; i < this.n; ++i)
      grdraw.vert(this.vert[i]);
  }

  void draw_edge() {
    for (int i = 0; i < this.n; ++i)
      for (int j = i + 1; j < this.n; ++j)
        grdraw.edge(this.vert[i], this.vert[j]);
  }

  void draw() {
    this.draw_vertices();
    this.draw_edge();
  }
}
