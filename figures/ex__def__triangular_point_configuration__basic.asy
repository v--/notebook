unitsize(1.5cm);

from notebook access PointLattice;

pair o = (0, 0);
pair u = (1, 0);
pair v = (1, sqrt(3)) / 2;

transform t = shift(-1.4u - 2.2v);

PointLattice lat = PointLattice(u=u, v=v, t=t);
lat.draw_on_subpic();

for (int n = 2; n <= 6; ++n) {
  draw(lat.subpic, t * o -- t * ((n - 1) * u) -- t * ((n - 1) * v) -- cycle);
}

lat.clip_subpic();
lat.draw_subpic();

newpage();

lat.clear_subpic();
lat.draw_on_subpic();

int n = 6;

clip(lat.subpic, t * (o - (u + v) / 2) -- t * ((n - 1) * u + (u + u - v) / 2) -- t * ((n - 1) * v + (v + v - u) / 2) -- cycle);

lat.clip_subpic(draw_frame=false);
lat.draw_subpic();
