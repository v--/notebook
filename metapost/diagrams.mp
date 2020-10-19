lax_bboxmargin := 4pt;
safe_arrow_spacing := 2.5pt;
safe_arrow_curvature := 10pt;

def line_midpoint = point 0.5 enddef;
def curve_midpoint = point 1 enddef;
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
def straight_arrow(expr src, dest) =
  center(src) -- center(dest) cutbefore lax_bbox(src) cutafter lax_bbox(dest);
enddef;

def curved_arrow(expr src, dest, shift) =
  center(src) .. 0.5 [center(src), center(dest)] + shift .. center(dest) cutbefore lax_bbox(src) cutafter lax_bbox(dest);
enddef;

def straight_arrow_shifted(expr src, dest, shift) =
  center(src) + shift -- center(dest) + shift cutbefore lax_bbox(src) cutafter lax_bbox(dest);
enddef;

% https://tex.stackexchange.com/questions/560673/fill-all-elements-of-a-metapost-array
def draw_nodes(suffix nodes) =
  i := 1;

  forever:
    if known(nodes[i]):
      draw(nodes[i]);
      i := i + 1;
    fi;

    exitif unknown(nodes[i]);
  endfor;
enddef;

def draw_arrows(suffix arrows) =
  i := 1;

  forever:
    if known(arrows[i]):
      drawarrow(arrows[i]);
      i := i + 1;
    fi;

    exitif unknown(arrows[i]);
  endfor;
enddef;

def draw_vertical_double_arrow(expr dest) =
  label("$\implies$", origin) rotated -90 shifted (dest - (1pt, 0));
enddef;
