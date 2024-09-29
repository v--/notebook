import 'asymptote/graphs.asy' as graphs;
import 'asymptote/graphs/cycle.asy' as CycleGraph;

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
    draw_vertex(this.a, L=a == '' ? '' : Label(a, align=2W));
    draw_vertex(this.b, L=b == '' ? '' : Label(b, align=2E));
    draw_vertex(this.c, L=c == '' ? '' : Label(c, align=2N));
  }

  void draw_edges(
    string ab = '',
    string ba = '',
    string bc = '',
    string cb = '',
    string ca = '',
    string ac = '',
    bool oriented = false
  ) {
    if (ba == '') {
      draw_edge(this.a, this.b, L=ab == '' ? '' : Label(ab, align=2S), is_arc=oriented);
    } else {
      draw_edge(this.b, this.a, L=Label(ba, align=2S), is_arc=oriented);
    }

    if (cb == '') {
      draw_edge(this.b, this.c, L=bc == '' ? '' : Label(bc, align=2E), is_arc=oriented);
    } else {
      draw_edge(this.c, this.b, L=Label(cb, align=2E), is_arc=oriented);
    }

    if (ac == '') {
      draw_edge(this.c, this.a, L=ca == '' ? '' : Label(ca, align=2W), is_arc=oriented);
    } else {
      draw_edge(this.a, this.c, L=Label(ac, align=2W), is_arc=oriented);
    }
  }
}
