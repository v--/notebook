unitsize(1.5cm);

from notebook access PointLattice;

pair o = (0, 0);
pair u = (1, 0);
pair v = (1, sqrt(3)) / 2;

transform t = rotate(90) * shift(-u / 2);
int n = 3;

PointLattice lat = PointLattice(u=u, v=v, t=t);
lat.draw_on_subpic();

draw(lat.subpic, t * (-n * v) -- t * (n * (v - u)) -- t * (n * u) -- cycle);

lat.clip_subpic();
lat.draw_subpic();

newpage();

lat.clear_subpic();
lat.draw_on_subpic();

clip(lat.subpic, t * (-(n + 0.5) * v) -- t * ((n + 0.5) * (v - u)) -- t * ((n + 0.5) * u) -- cycle);

lat.clip_subpic(draw_frame=false);
lat.draw_subpic();
