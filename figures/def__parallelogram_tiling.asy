unitsize(1.5cm);

from notebook access PointLattice;

void draw_tiling(pair u, pair v) {
  transform t = shift(-(u + v) / 2);

  PointLattice lat = PointLattice(u=u, v=v, n=3, unit_size=1cm, t=t);
  path pth = (0, 0) -- u -- (u + v) -- v -- cycle;

  lat.draw_on_subpic(pth_fillpen=nullpen, pth=pth);

  label(t * (0, 0), '$A$', align=SW, pic=lat.subpic);
  label(t * u,      '$B$', align=SE, pic=lat.subpic);
  label(t * u + v,  '$C$', align=NE, pic=lat.subpic);
  label(t * v,      '$D$', align=NW, pic=lat.subpic);

  fill(lat.subpic, t * pth, mediumgray);
  draw(lat.subpic, t * pth, gray);

  lat.draw_on_subpic(draw_dots=true);
  lat.clip_subpic();
  lat.draw_subpic();
}

draw_tiling(
  u=(1, 0),
  v=(0, 1)
);

newpage();

draw_tiling(
  u=(1, 0),
  v=(1, sqrt(3)) / 2
);
