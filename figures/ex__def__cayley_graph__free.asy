unitsize(1.5cm);

from geometry access defaultcoordsys;
from notebook access grdraw;

void draw_tree(pair o, int arity, real radius, int depth, int source = 0) {
  if (depth == 0) {
    grdraw.vert(o);
    return;
  }

  for (int i = 1; i < 2arity + 1; ++i) {
    if (source > 0 && (i - source) % 2arity == arity) {
      continue;
    }

    real angle = (i - 1) / arity * pi;
    pair p = o + defaultcoordsys.polar(radius, angle);

    if (i <= arity) {
      grdraw.edge(o, p, is_arc=true, dash=i % 2 == 0);
    } else {
      grdraw.edge(p, o, is_arc=true, dash=i % 2 == 0);
    }

    draw_tree(p, arity, radius / 2, depth - 1, source=i);
  }

  grdraw.vert(o);
}

draw_tree((0, 0), arity=2, radius=1.5, depth=4);
