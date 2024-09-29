import patterns;
import 'asymptote/polar.asy' as polar;

pen densely_dashed = linetype(new real[] { 2, 2 });
pen vert_label = fontsize(10);
pen edge_label = fontsize(9);
pen regular_edge = linewidth(0.5);
pen bold_edge = linewidth(1);
real dot_radius = 0.04;

add('hyperedge_pattern', hatch(0.75mm, lightgray));

void draw_vertex(
  pair v,
  Label L = '',
  pen color = white
) {
  filldraw(
    shift(v) * scale(dot_radius) * unitcircle,
    regular_edge + color
  );

  if (L != '') {
    label(L, v, vert_label);
  }
}

void _draw_edge_impl(
  path pth,
  Label L = '',
  pen color = black,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pen p = (dash ? densely_dashed : currentpen) + color + linecap(0);
  draw(pth, p=p + (bold ? bold_edge : regular_edge));

  if (is_arc) {
    arrowbar arrow = Arrow(size=4, angle=20, filltype=null);
    draw(pth, p=p, arrow=arrow);
  }

  if (L != '') {
    label(L, pth, edge_label);
  }
}

pair _bend_midpoint(pair u, pair v, real bend = 0, real bend_at = 1 / 2) {
  pair d = v - u;
  pair n = d.x == 0 ? (1, 0) : (d.y / d.x, -1);
  return bend_at * (u + v) + n * bend;
}

pair _shift_for_dot(pair u, pair v, real by = dot_radius) {
  return by * (v - u) / length(v - u);
}

void draw_edge(
  pair u,
  pair v,
  real bend = 0,
  real bend_at = 0.5,
  Label L = '',
  pen color = black,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pair mid = _bend_midpoint(u, v, bend=bend, bend_at=bend_at);
  pair u_ = u + _shift_for_dot(u, mid);
  pair v_ = v - _shift_for_dot(mid, v);

  _draw_edge_impl(
    u_ .. mid .. v_,
    L=L, color=color, dash=dash, bold=bold, is_arc=is_arc
  );
}

void draw_loop(
  pair v,
  Label L = '',
  pen color = black,
  real angle = 0,
  bool dash = false,
  bool bold = false,
  bool is_arc = false
) {
  pair m = v + 0.4 * polar(angle);
  pair v_ = v + _shift_for_dot(v, m);

  _draw_edge_impl(
    v_ .. _bend_midpoint(v_, m, bend=0.05) .. m .. _bend_midpoint(v_, m, bend=-0.05) .. v_,
    L=L, color=color, dash=dash, bold=bold, is_arc=is_arc
  );
}

void draw_hyperedge(
  pair[] vert,
  Label L = '',
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
    outline = outline -- v + _shift_for_dot(v, w) -- w - _shift_for_dot(v, w);
  }

  outline = outline -- cycle;

  filldraw(
    outline,
    drawpen=(dash ? densely_dashed : currentpen) + (bold ? bold_edge : regular_edge),
    fillpen=pattern('hyperedge_pattern') + red
  );

  if (L != '') {
    label(mean, L, edge_label);
  }
}
