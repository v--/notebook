import geometry;

access 'asymptote/num.asy' as num;

void angle_dot(point P, point O, point Q, real radius=10, pen p=currentpen, picture pic=currentpicture) {
  picture subpic; // This subpicture allows us to not depend on the unit size
  point d = unit((length((Q - O)) * (P - O) + length(P - O) * (Q - O)) / 2);
  dot(subpic, (radius / 2 + linewidth(p)) * d, p + 2linewidth(p));
  add(pic, subpic, O);
}

void mark_angle(point P, point O, point Q, real radius=10, bool orth_dot = true, pen p=currentpen, picture pic=currentpicture, Label L='', arrowbar arrow = None) {
  markangle(P, O, Q, radius=radius, p=p, pic=pic, L=L, arrow=arrow);

  if (orth_dot && num.is_nearly_zero(abs(dot(P - O, Q - O)))) {
    angle_dot(P, O, Q, radius=radius, p=p, pic=pic);
  }
}
