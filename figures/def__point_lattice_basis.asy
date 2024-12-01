unitsize(1.5cm);

from notebook access PointLattice;

pair u = unit((1, -0.1));
pair v = unit((1, 1));

PointLattice lat = PointLattice(u=u, v=v);
lat.draw();

newpage();

lat.draw(draw_grid=true, draw_basis=true);

newpage();

PointLattice lat = PointLattice(u=u, v=v - u);
lat.draw(draw_grid=true, draw_basis=true);
