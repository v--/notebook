unitsize(0.5cm);

from notebook access PointLattice, pens, assets;

PointLattice lat = PointLattice(
  u=(1, 0),
  v=(0, 1)
);

filldraw(
  assets.get_cross(extent=1.5, thickness=0.5),
  fillpen=pens.ne_hatch
);

lat.draw();

newpage();

lat.clear_subpic();

filldraw(
  assets.get_cross(extent=lat.n, thickness=0.5),
  fillpen=pens.ne_hatch,
  pic=lat.subpic
);

lat.draw_on_subpic();
lat.clip_subpic();
lat.draw_subpic();
