import 'asymptote/polar.asy' as polar;
import 'asymptote/graphs.asy' as graphs;

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
      draw_vertex(this.left[i]);

    for (int j = 0; j < this.m; ++j)
      draw_vertex(this.right[j]);
  }

  void draw_edges_complete() {
    for (int i = 0; i < this.n; ++i)
      for (int j = 0; j < this.m; ++j)
        draw_edge(this.left[i], this.right[j]);
  }
}