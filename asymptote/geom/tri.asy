import geometry;

access 'asymptote/lab.asy' as lab;
from 'asymptote/geom/angles.asy' access mark_angle;

void draw_vertices(triangle tri, bool draw_labels = true, string a='$A$', string b='$B$', string c='$C$') {
  if (draw_labels) {
    dot(tri.A, L=Label(a, align=lab.align_oppose(tri.A, midpoint(tri.BC))));
    dot(tri.B, L=Label(b, align=lab.align_oppose(tri.B, midpoint(tri.AC))));
    dot(tri.C, L=Label(c, align=lab.align_oppose(tri.C, midpoint(tri.AB))));
  } else {
    dot(tri.A);
    dot(tri.B);
    dot(tri.C);
  }
}

void mark_angles(triangle tri, string a='$\\alpha$', string b='$\\beta$', string c='$\\gamma$') {
  mark_angle(
    tri.B, tri.A, tri.C,
    L=Label(a)
  );

  mark_angle(
    tri.C, tri.B, tri.A,
    L=Label(b)
  );

  mark_angle(
    tri.A, tri.C, tri.B,
    L=Label(c)
  );
}
