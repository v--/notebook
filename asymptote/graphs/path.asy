from geometry access defaultcoordsys;

access 'asymptote/graphs/grdraw.asy' as grdraw;

struct PathGraph {
  int n;
  pair[] vert;

  void operator init(int n, real dist = 0.75, real angle = 0) {
    this.n = n;

    pair d = defaultcoordsys.polar(1, angle);

    for (int i = 0; i < n; ++i) {
      this.vert[i] = i * dist * d;
    }
  }

  void draw() {
    for (int i = 0; i < this.n; ++i)
      grdraw.vert(this.vert[i]);

    for (int i = 0; i < this.n - 1; ++i)
      grdraw.edge(this.vert[i], this.vert[i + 1]);
  }
}
