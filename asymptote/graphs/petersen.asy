import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/cycle.asy' as CycleGraph;

struct PetersenGraph {
  int n;
  int m;
  pair[] outer;
  pair[] inner;

  void operator init(int n, int m, real outer_radius = 1, real inner_radius = 0.5) {
    this.n = n;
    this.m = m;

    if (n == 2) {
      this.outer = new pair[] {
        (-outer_radius, 0),
        (outer_radius, 0)
      };

      this.inner = new pair[] {
        (-inner_radius, -inner_radius),
        (inner_radius, -inner_radius)
      };

      return;
    }

    this.outer = CycleGraph(n, outer_radius).vert;

    for (int i = 0; i < n; ++i)
      this.inner[i] = inner_radius / outer_radius * this.outer[i];
  }

  void draw() {
    for (int i = 0; i < this.n; ++i) {
      draw_vertex(this.outer[i]);
      draw_vertex(this.inner[i]);
    }

    for (int i = 0; i < this.n; ++i) {
      draw_edge(this.outer[i], this.outer[(i + 1) % this.n]);
      draw_edge(this.outer[i], this.inner[i % this.n]);
      draw_edge(this.inner[i], this.inner[(i + this.m) % this.n]);
    }
  }
}
