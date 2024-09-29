import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/cycle.asy' as CycleGraph;

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
    draw_vertex(this.origin);

    for (int i = 0; i < this.n; ++i)
      draw_vertex(this.vert[i]);
  }

  void draw_edges() {
    for (int i = 0; i < this.n; ++i)
      draw_edge(this.origin, this.vert[i]);
  }
}
