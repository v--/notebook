import 'asymptote/math.asy' as math;

pen densely_dashed = linetype(new real[] { 2, 4 });

void draw_vertex(
  pair v,
  Label L = ""
) {
  dot(v, L=L, filltype=FillDraw(fillpen=white, drawpen=black), p=linewidth(0.75));
}

void _draw_edge_impl(
  path pth,
  Label L = "",
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  draw(
    pth,
    p=(dash ? densely_dashed : currentpen) + linewidth(bold ? 1 : 0.5) + fontsize(9),
    L=L,
    arrow=is_arc ? ArcArrow(HookHead, size=2) : None
  );
}

pair _bend_midpoint(pair u, pair v, real bend = 0) {
  pair d = v - u;
  pair n = d.x == 0 ? (1, 0) : (d.y / d.x, -1);
  return (u + v) / 2 + n * bend;
}

pair _shift_for_dot(pair u, pair v) {
  return 0.05 * (v - u) / norm(v - u);
}

void draw_edge(
  pair u,
  pair v,
  real bend = 0,
  Label L = "",
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pair m = _bend_midpoint(u, v, bend=bend);
  pair u_ = u + _shift_for_dot(u, m);
  pair v_ = v - _shift_for_dot(m, v);

  _draw_edge_impl(
    u_ .. m .. v_,
    L=L, dash=dash, bold=bold, is_arc=is_arc
  );
}

void draw_loop(
  pair v,
  Label L = "",
  real angle = 0,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pair m = v + 0.4 * (cos(angle), sin(angle));
  pair v_ = v + _shift_for_dot(v, m);

  _draw_edge_impl(
    v_ .. _bend_midpoint(v_, m, bend=0.05) .. m .. _bend_midpoint(v_, m, bend=-0.05) .. v_,
    L=L, dash=dash, bold=bold, is_arc=is_arc
  );
}
