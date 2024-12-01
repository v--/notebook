import geometry;

access 'asymptote/lab.asy' as lab;
from 'asymptote/geom/angles.asy' access mark_angle;

void draw_vertices(triangle tri, bool draw_labels = true) {
  if (draw_labels) {
    dot(tri.A, L=Label('$A$', align=lab.align_oppose(tri.A, midpoint(tri.BC))));
    dot(tri.B, L=Label('$B$', align=lab.align_oppose(tri.B, midpoint(tri.AC))));
    dot(tri.C, L=Label('$C$', align=lab.align_oppose(tri.C, midpoint(tri.AB))));
  } else {
    dot(tri.A);
    dot(tri.B);
    dot(tri.C);
  }
}

void mark_angles(triangle tri) {
  mark_angle(
    tri.B, tri.A, tri.C,
    L=Label('$\\alpha$')
  );

  mark_angle(
    tri.C, tri.B, tri.A,
    L=Label('$\\beta$')
  );

  mark_angle(
    tri.A, tri.C, tri.B,
    L=Label('$\\gamma$')
  );
}
