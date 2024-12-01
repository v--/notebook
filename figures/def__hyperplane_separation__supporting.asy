unitsize(1cm);

draw(unitcircle, L=Label('$A$', align=S, position=1));

transform rot(real angle) {
  return (
    0, 0,
    cos(angle), -sin(angle),
    sin(angle), cos(angle)
  );
};

for (int k = -4; k <= 4; ++k) {
  transform T = rot(2pi + k * pi / 16);
  draw(T * (-2, -1) -- T * (2, -1));
}
