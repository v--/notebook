lax_bboxmargin := 4pt;
safe_arc_spacing := 2.5pt;
safe_arc_curvature := 10pt;

def straight_arc_midpoint = point 0.5 enddef;
def curved_arc_midpoint = point 1 enddef;
def dotted = dashed withdots scaled 0.5 enddef;

def lax_bbox(expr p) :=
  (
    llcorner(p) + (-1, -1) * lax_bboxmargin --
    lrcorner(p) + (1, -1) * lax_bboxmargin --
    urcorner(p) + (1, 1) * lax_bboxmargin --
    ulcorner(p) + (-1, 1) * lax_bboxmargin --
    cycle
  )
enddef;

% https://tex.stackexchange.com/questions/284785/drawing-non-trivial-commutative-diagrams
def straight_arc(expr src, dest) =
  center(src) -- center(dest) cutbefore lax_bbox(src) cutafter lax_bbox(dest);
enddef;

def curved_arc(expr src, dest, shift) =
  center(src) .. 0.5 [center(src), center(dest)] + shift .. center(dest) cutbefore lax_bbox(src) cutafter lax_bbox(dest);
enddef;

def straight_arc_shifted(expr src, dest, shift) =
  center(src) + shift -- center(dest) + shift cutbefore lax_bbox(src) cutafter lax_bbox(dest);
enddef;

% https://tex.stackexchange.com/questions/560673/fill-all-elements-of-a-metapost-array
def draw_vertices(suffix vertices) =
  i := 1;

  forever:
    if known(vertices[i]):
      draw(vertices[i]);
      i := i + 1;
    fi;

    exitif unknown(vertices[i]);
  endfor;
enddef;

def draw_arcs(suffix arcs) =
  i := 1;

  forever:
    if known(arcs[i]):
      drawarrow(arcs[i]);
      i := i + 1;
    fi;

    exitif unknown(arcs[i]);
  endfor;
enddef;

def draw_edges(suffix arcs) =
  i := 1;

  forever:
    if known(arcs[i]):
      draw(arcs[i]);
      i := i + 1;
    fi;

    exitif unknown(arcs[i]);
  endfor;
enddef;

def draw_vertical_double_arc(expr dest) =
  label("$\implies$", origin) rotated -90 shifted (dest - (1pt, 0));
enddef;
