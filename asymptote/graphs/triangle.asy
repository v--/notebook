access 'asymptote/graphs/grdraw.asy' as grdraw;
from 'asymptote/graphs/cycle.asy' access CycleGraph;

struct TriangleGraph {
  pair a;
  pair b;
  pair c;

  void operator init(real radius = 0.75) {
    CycleGraph cg = CycleGraph(3, radius);

    this.a = cg.vert[0];
    this.b = cg.vert[1];
    this.c = cg.vert[2];
  }

  void draw_vertices(string a = '', string b = '', string c = '') {
    grdraw.vert(this.a, L=a == '' ? '' : Label(a, align=2W));
    grdraw.vert(this.b, L=b == '' ? '' : Label(b, align=2E));
    grdraw.vert(this.c, L=c == '' ? '' : Label(c, align=2N));
  }

  void draw_edge(
    string ab = '',
    string ba = '',
    string bc = '',
    string cb = '',
    string ca = '',
    string ac = '',
    bool oriented = false
  ) {
    if (ba == '') {
      grdraw.edge(this.a, this.b, L=ab == '' ? '' : Label(ab, align=2S), is_arc=oriented);
    } else {
      grdraw.edge(this.b, this.a, L=Label(ba, align=2S), is_arc=oriented);
    }

    if (cb == '') {
      grdraw.edge(this.b, this.c, L=bc == '' ? '' : Label(bc, align=2E), is_arc=oriented);
    } else {
      grdraw.edge(this.c, this.b, L=Label(cb, align=2E), is_arc=oriented);
    }

    if (ac == '') {
      grdraw.edge(this.c, this.a, L=ca == '' ? '' : Label(ca, align=2W), is_arc=oriented);
    } else {
      grdraw.edge(this.a, this.c, L=Label(ac, align=2W), is_arc=oriented);
    }
  }
}
