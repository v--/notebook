unitsize(1.5cm);

from notebook access PointLattice;

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(0, 1),
  n=4,
  unit_size=1cm
);

lat.draw_on_subpic(draw_dots=false, draw_grid=true);

dot(lat.subpic, (0, 0));
dot(lat.subpic, (1, 0));
dot(lat.subpic, (-1, 0));
dot(lat.subpic, (0, 1));
dot(lat.subpic, (0, -1));

lat.clip_subpic();
lat.draw_subpic();

newpage();

lat.draw_on_subpic(draw_dots=false, draw_grid=true);

for (int i = -1; i <= 1; ++i) {
  for (int j = -1; j <= 1; ++j) {
    dot(lat.subpic, (i, j));
  }
}

lat.clip_subpic();
lat.draw_subpic();
