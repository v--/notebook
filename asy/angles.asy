void angle_dot(pair P, pair O, pair Q, real radius=5, pen p=currentpen, picture pic=currentpicture) {
  import geometry;

  picture subpic; // This subpicture allows us to not depend on the unit size
  pair d = unit((length((Q - O)) * (P - O) + length(P - O) * (Q - O)) / 2);
  dot(subpic, (radius / 2 + linewidth(p)) * d, p + 2linewidth(p));
  add(pic, subpic, O);
}

pair orth_proj(pair P, pair O, pair d) {
  return O + (d.x * (P - O).x + d.y * (P - O).y) * d / length(d)^2;
}
