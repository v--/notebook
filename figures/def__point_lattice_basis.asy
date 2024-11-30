usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/point_lattices.asy' as point_lattices;

pair u = unit((1, -0.1));
pair v = unit((1, 1));

PointLattice lat = PointLattice(u=u, v=v);
lat.draw();

newpage();

lat.draw(draw_grid=true, draw_basis=true);

newpage();

PointLattice lat = PointLattice(u=u, v=v - u);
lat.draw(draw_grid=true, draw_basis=true);
