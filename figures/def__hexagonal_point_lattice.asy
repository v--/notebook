unitsize(1.5cm);

from notebook access geom, PointLattice;

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(1, sqrt(3)) / 2
);

lat.draw(draw_grid=true, draw_basis=true);

newpage();

lat.draw(
  draw_grid=true,
  draw_basis=true,
  pth=rotate(30) * geom.regular_polygon(6, 1 / sqrt(3)),
  pth_fillpen=nullpen
);
