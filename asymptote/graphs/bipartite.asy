access 'asymptote/graphs/grdraw.asy' as grdraw;

struct BipartiteGraph {
  int n;
  int m;
  pair[] left;
  pair[] right;

  void operator init(int n, int m, real xdist = 0.75, real ydist = 0.75) {
    this.n = n;
    this.m = m;

    for (int i = 0; i < n; ++i) {
      this.left[i] = (0, (i - n / 2) * ydist);
    }

    for (int j = 0; j < m; ++j) {
      this.right[j] = (xdist, (j - m / 2) * ydist);
    }
  }

  void draw_vertices() {
    for (int i = 0; i < this.n; ++i)
      grdraw.vert(this.left[i]);

    for (int j = 0; j < this.m; ++j)
      grdraw.vert(this.right[j]);
  }

  void draw_edge_complete() {
    for (int i = 0; i < this.n; ++i)
      for (int j = 0; j < this.m; ++j)
        grdraw.edge(this.left[i], this.right[j]);
  }
}
