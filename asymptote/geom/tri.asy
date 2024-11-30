import geometry;

import 'asymptote/labels.asy' as labels;

void draw_vertices(triangle tri, bool draw_labels = true) {
  if (draw_labels) {
    dot(tri.A, L=Label('$A$', align=align_oppose(tri.A, midpoint(tri.BC))));
    dot(tri.B, L=Label('$B$', align=align_oppose(tri.B, midpoint(tri.AC))));
    dot(tri.C, L=Label('$C$', align=align_oppose(tri.C, midpoint(tri.AB))));
  } else {
    dot(tri.A);
    dot(tri.B);
    dot(tri.C);
  }
}

void draw_angles(triangle tri) {
  markangle(
    tri.B, tri.A, tri.C,
    radius=10,
    L=Label('$\\alpha$')
  );

  markangle(
    tri.C, tri.B, tri.A,
    radius=10,
    L=Label('$\\beta$')
  );

  markangle(
    tri.A, tri.C, tri.B,
    radius=10,
    L=Label('$\\gamma$')
  );
}
