usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/point_lattices.asy' as point_lattices;

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
