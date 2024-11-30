usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/point_lattices.asy' as point_lattices;

path circ = scale(0.5) * unitcircle;

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(0, 1)
);

lat.draw(pth=circ);

newpage();

PointLattice lat = PointLattice(
  u=(1.6, 0),
  v=(0.5, 0.5) * sqrt(2)
);

lat.draw(pth=circ);

newpage();

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(1, sqrt(3)) / 2
);

lat.draw(pth=circ);
