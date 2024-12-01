access 'asymptote/graphs/grdraw.asy' as grdraw;
from 'asymptote/graphs/cycle.asy' access CycleGraph;

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
      grdraw.vert(this.outer[i]);
      grdraw.vert(this.inner[i]);
    }

    for (int i = 0; i < this.n; ++i) {
      grdraw.edge(this.outer[i], this.outer[(i + 1) % this.n]);
      grdraw.edge(this.outer[i], this.inner[i % this.n]);
      grdraw.edge(this.inner[i], this.inner[(i + this.m) % this.n]);
    }
  }
}
