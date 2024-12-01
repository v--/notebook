unitsize(1.5cm);

from notebook access PointLattice;

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(0, 1)
);

lat.draw();

newpage();

lat.draw(draw_grid=true, draw_basis=true);

newpage();

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(1, 1)
);

lat.draw(draw_grid=true, draw_basis=true);
