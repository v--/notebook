access 'asymptote/graphs/grdraw.asy' as grdraw;
from 'asymptote/graphs/cycle.asy' access CycleGraph;

struct SquareGraph {
  pair a;
  pair b;
  pair c;
  pair d;

  void operator init(real dist = 0.75) {
    this.a = (0, 0);
    this.b = (dist, 0);
    this.c = (dist, dist);
    this.d = (0, dist);
  }

  void draw_vertices(string a = '', string b = '', string c = '', string d = '') {
    grdraw.vert(this.a, L=a == '' ? '' : Label(a, align=2W));
    grdraw.vert(this.b, L=b == '' ? '' : Label(b, align=2E));
    grdraw.vert(this.c, L=c == '' ? '' : Label(c, align=2E));
    grdraw.vert(this.d, L=d == '' ? '' : Label(d, align=2W));
  }

  void draw_edge(
    string ab = '',
    string ba = '',
    string bc = '',
    string cb = '',
    string cd = '',
    string dc = '',
    string da = '',
    string ad = '',
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

    if (dc == '') {
      grdraw.edge(this.c, this.d, L=cd == '' ? '' : Label(cd, align=2N), is_arc=oriented);
    } else {
      grdraw.edge(this.d, this.c, L=Label(dc, align=2N), is_arc=oriented);
    }

    if (ad == '') {
      grdraw.edge(this.d, this.a, L=da == '' ? '' : Label(da, align=2W), is_arc=oriented);
    } else {
      grdraw.edge(this.a, this.d, L=Label(ad, align=2W), is_arc=oriented);
    }
  }
}
