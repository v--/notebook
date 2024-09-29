import 'asymptote/polar.asy' as polar;
import 'asymptote/graphs.asy' as graphs;

struct PathGraph {
  int n;
  pair[] vert;

  void operator init(int n, real dist = 0.75, real angle = 0) {
    this.n = n;

    pair d = polar(angle);

    for (int i = 0; i < n; ++i) {
      this.vert[i] = i * dist * d;
    }
  }

  void draw() {
    for (int i = 0; i < this.n; ++i)
      draw_vertex(this.vert[i]);

    for (int i = 0; i < this.n - 1; ++i)
      draw_edge(this.vert[i], this.vert[i + 1]);
  }
}
