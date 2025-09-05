access graph;
access patterns;
from geometry access defaultcoordsys;

access 'asymptote/pens.asy' as pens;

pen vert_label = fontsize(10);
pen edge_label = fontsize(9);
pen regular_edge = linewidth(0.5);
pen bold_edge = linewidth(2);
real dot_radius = 0.08;

void vert(
  pair v,
  Label L = '',
  pen p = white
) {
  filldraw(
    shift(v) * scale(dot_radius) * unitcircle,
    regular_edge + p
  );

  if (L != '') {
    label(L, v, vert_label);
  }
}

void _draw_edge_impl(
  path pth,
  Label L = '',
  pen p = black,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pen p = (dash ? pens.densely_dashed : currentpen) + (bold ? bold_edge : regular_edge) + linecap(0) + p;

  if (is_arc) {
    arrowbar arrow = Arrow(size=(bold ? 5 : 4), angle=(bold ? 30 : 20), filltype=FillDraw(drawpen=linecap(0)));
    draw(pth, p=p, arrow);
  } else {
    draw(pth, p=p);
  }

  if (L != '') {
    label(L, pth, edge_label);
  }
}

pair _bend_midpoint(pair u, pair v, real bend = 0, real bend_at = 0.5) {
  pair d = v - u;
  pair n = (0, 1);

  if (d.y != 0) {
    int sign = (d.y > 0) ? 1 : -1;
    n = sign * unit((-1, d.x / d.y));
  }

  return bend_at * v + (1 - bend_at) * u + n * bend;
}

pair _shift_for_dot(pair u, pair v, real vertex_offset = dot_radius) {
  return vertex_offset * (v - u) / length(v - u);
}

void edge(
  pair u,
  pair v,
  real bend = 0,
  real bend_at = 0.5,
  real vertex_offset = dot_radius,
  Label L = '',
  pen p = black,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pair mid = _bend_midpoint(u, v, bend=bend, bend_at=bend_at);
  pair u_ = u + _shift_for_dot(u, mid, vertex_offset);
  pair v_ = v - _shift_for_dot(mid, v, vertex_offset);

  _draw_edge_impl(
    u_ .. mid .. v_,
    L=L, p=p, dash=dash, bold=bold, is_arc=is_arc
  );
}

void loop(
  pair v,
  Label L = '',
  pen p = black,
  real angle = 0,
  real vertex_offset = dot_radius,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pair m = v + defaultcoordsys.polar(0.4, angle);
  pair v_ = v + _shift_for_dot(v, m, vertex_offset);

  _draw_edge_impl(
    v_ .. _bend_midpoint(v_, m, bend=0.05) .. m .. _bend_midpoint(v_, m, bend=-0.05) .. v_,
    L=L, p=p, dash=dash, bold=bold, is_arc=is_arc
  );
}

void hyperedge(
  pair[] vert,
  Label L = '',
  real vertex_offset = dot_radius,
  bool dash = false,
  bool bold = false
) {
  path outline = nullpath;
  pair mean = (0, 0);

  for (int i = 0; i < vert.length; ++i) {
    pair v = vert[i];

    mean += v / vert.length;

    pair u = vert[(i - 1) % vert.length];
    pair w = vert[(i + 1) % vert.length];

    outline = outline -- arc(v, dot_radius, degrees(u - v), degrees(w - v));
    outline = outline -- v + _shift_for_dot(v, w, vertex_offset) -- w - _shift_for_dot(v, w, vertex_offset);
  }

  outline = outline -- cycle;

  filldraw(
    outline,
    drawpen=(dash ? pens.densely_dashed : currentpen) + (bold ? bold_edge : regular_edge),
    fillpen=pens.ne_hatch
  );

  if (L != '') {
    label(mean, L, edge_label);
  }
}
