from geometry access defaultcoordsys;

access 'asymptote/graphs/grdraw.asy' as grdraw;

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
      this.vert[i] = defaultcoordsys.polar(radius, angle);
    }
  }

  void draw_vertices() {
    for (int i = 0; i < this.n; ++i)
      grdraw.vert(this.vert[i]);
  }

  void draw_edge() {
    for (int i = 0; i < this.n; ++i)
      grdraw.edge(this.vert[i], this.vert[(i + 1) % this.n]);
  }

  void draw() {
    this.draw_vertices();
    this.draw_edge();
  }
}
