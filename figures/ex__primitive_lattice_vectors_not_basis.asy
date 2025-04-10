unitsize(1.5cm);

from notebook access PointLattice;

pair o = (0, 0);
pair u = (1, 0);
pair v = (1, sqrt(3)) / 2;

PointLattice lat = PointLattice(u=u, v=v);
lat.draw(draw_basis=true, draw_grid=true);

newpage();

lat.draw();
PointLattice sublat = PointLattice(u=u + v, v=u - v);
sublat.draw(draw_basis=true, draw_grid=true);
