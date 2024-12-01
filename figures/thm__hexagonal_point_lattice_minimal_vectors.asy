unitsize(1.5cm);

import graph;

from notebook access geom, PointLattice;

int n = 6;

pair o = (0, 0);
pair u = (1, 0);
pair v = rotate(60) * u;

PointLattice lat = PointLattice(u=u, v=v, n=4, unit_size=1cm);

string[] labels = new string[] { '$u$', '$v$', '$v - u$', '$-u$', '$-v$', '$u - v$' };

lat.draw_on_subpic(dot_drawpen=mediumgray);
dot(lat.subpic, o);

for (int k = 0; k < n; ++k) {
  pair w = rotate(60k) * u;
  dot(lat.subpic, w);
  draw(lat.subpic, o -- w);
  label(pic=lat.subpic, w, labels[k], align=2w);
}

lat.clip_subpic();
lat.draw_subpic();
