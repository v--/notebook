usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/point_lattices.asy' as point_lattices;
import 'asymptote/polygons.asy' as polygons;

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(1, sqrt(3)) / 2
);

lat.draw(draw_grid=true, draw_basis=true);

newpage();

lat.draw(
  draw_grid=true,
  draw_basis=true,
  pth=rotate(30) * regular_polygon(6, 1 / sqrt(3)),
  pth_fillpen=nullpen
);
