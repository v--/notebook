import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/cycle.asy' as CycleGraph;

struct CompleteGraph {
  int n;
  pair[] vert;

  void operator init(int n, real radius = 0.75) {
    this.n = n;

    if (n == 4) {
      this.vert = CycleGraph(3, radius).vert;
      this.vert[3] = (0, 0);
    } else {
      this.vert = CycleGraph(n, radius).vert;
    }
  }

  void draw_vertices() {
    for (int i = 0; i < this.n; ++i)
      draw_vertex(this.vert[i]);
  }

  void draw_edges() {
    for (int i = 0; i < this.n; ++i)
      for (int j = i + 1; j < this.n; ++j)
        draw_edge(this.vert[i], this.vert[j]);
  }

  void draw() {
    this.draw_vertices();
    this.draw_edges();
  }
}
