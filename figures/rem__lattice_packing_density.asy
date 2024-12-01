unitsize(1.5cm);

from notebook access blobs, PointLattice;

pair u = (1, 0.3);
pair v = (0.3, 1);

PointLattice lat = PointLattice(u=u, v=v, n=2, unit_size=1cm);
lat.draw(pth=blobs.blob1, draw_grid=true, draw_basis=true);

newpage();

PointLattice lat = PointLattice(u=u - v, v=v, n=2, unit_size=1cm);
lat.draw(pth=blobs.blob1, draw_grid=true, draw_basis=true);
