unitsize(1.5cm);

from notebook access geom, pens, PointLattice;

void draw_tiling(pair u) {
  pair v = rotate(60) * u;
  transform rot = rotate(degrees(atan2(u.y, u.x)) + 30);

  PointLattice lat = PointLattice(u=u, v=v, n=3, unit_size=1cm);

  path pol = rot * geom.regular_polygon(6, 1 / sqrt(3));

  lat.draw_on_subpic(draw_dots=true, pth_fillpen=nullpen, pth=pol);

  pair O = (0, 0);
  pair B = rot * (sqrt(3) / 3, 0);
  pair A = rotate(-60) * B;

  fill(lat.subpic, pol, mediumgray);
  draw(lat.subpic, pol, gray);

  lat.clip_subpic();
  lat.draw_subpic();
}

pair u = (1, 0);

draw_tiling(u);

newpage();

PointLattice sublat = PointLattice(u=u, v=rotate(60) * u, n=3, unit_size=1cm);

sublat.draw(
  draw_dots=false,
  pth=scale(1 / 2) * unitcircle
);

draw_tiling(u);
