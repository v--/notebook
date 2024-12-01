access 'asymptote/graphs/grdraw.asy' as grdraw;

struct ExampleFlowGraph {
  pair v1;
  pair v2;
  pair v3;
  pair v4;
  pair v5;
  pair v6;

  void operator init() {
    this.v1 = (0, 0);
    this.v2 = (1, 1);
    this.v3 = (1, -1);
    this.v4 = (3, 1);
    this.v5 = (3, -1);
    this.v6 = (4, 0);
  }

  void draw_vertices(bool shift_v6) {
    grdraw.vert(this.v1, L=Label('$v_1$', align=2W));
    grdraw.vert(this.v2, L=Label('$v_2$', align=2N));
    grdraw.vert(this.v3, L=Label('$v_3$', align=2S));
    grdraw.vert(this.v4, L=Label('$v_4$', align=2N));
    grdraw.vert(this.v5, L=Label('$v_5$', align=2S));
    grdraw.vert(this.v6, L=Label('$v_6$', align=shift_v6 ? 2S : 2E));
  }
}
