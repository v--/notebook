usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/graphs.asy' as graphs;
import 'asymptote/point_lattices.asy' as point_lattices;

pair o = (0, 0);
pair u = (1, 0);
pair v = (0, 1);

int lim = 5;

transform t = shift(-2.5(u + v));

PointLattice lat = PointLattice(u=u, v=v, t=t, n=7);
lat.draw_on_subpic();

for (int n = 1; n <= 5; ++n) {
  draw(lat.subpic, t * o -- t * (n * u) -- t * (n * (u + v)) -- t * (n * v) -- cycle);
}

lat.clip_subpic();
lat.draw_subpic();

newpage();

lat.clear_subpic();
lat.draw_on_subpic();

int n = 6;

clip(lat.subpic, t * (o - (u + v) / 2) -- t * ((n - 1) * u + (u - v) / 2) -- t * ((n - 1) * (u + v) + (u + v) / 2) -- t * ((n - 1) * v + (v - u) / 2) -- cycle);

lat.clip_subpic(draw_frame=false);
lat.draw_subpic();
