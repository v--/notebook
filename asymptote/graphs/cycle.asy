import 'asymptote/polar.asy' as polar;
import 'asymptote/graphs.asy' as graphs;

struct CycleGraph {
  int n;
  pair[] vert;

  void operator init(int n, real radius = 0.75) {
    this.n = n;

    // The following correction ensures that the figure is "upright"
    real base_angle = 3 / 2 * pi;
    real next_angle = (3 / 4 + 1 / n) * 2 * pi;
    real correction = -(base_angle + next_angle) / 2;

    for (int i = 0; i < n; ++i) {
      real angle = base_angle + correction + (3 / 4 + i / n) * 2 * pi;
      this.vert[i] = radius * polar(angle);
    }
  }

  void draw_vertices() {
    for (int i = 0; i < this.n; ++i)
      draw_vertex(this.vert[i]);
  }

  void draw_edges() {
    for (int i = 0; i < this.n; ++i)
      draw_edge(this.vert[i], this.vert[(i + 1) % this.n]);
  }

  void draw() {
    this.draw_vertices();
    this.draw_edges();
  }
}