unitsize(2cm);

import three;

from notebook access trj;

currentprojection = orthographic(camera=(-0.2, 0.3, 0.2));

transform3 T = {
  {1, 0, 0, 0},
  {0, 4 / 5, -2 / 5, -1 / 5},
  {0, -2 / 5, 1 / 5, -2 / 5},
  {0, 0, 0, 1}
};

path plane_path = (-1 / 2, -1) -- (-1 / 2, 3 / 2) -- (3 / 2, 3 / 2) -- (3 / 2, -1) -- cycle;
path plane_hole = (0, -1 / 2) -- (0, 1) -- (1, 1) -- (1, -1 / 2) -- cycle;

if (settings.render == 0) {
  draw(T * surface(plane_path), white);
  draw(T * surface(plane_hole), mediumgray);
} else {
  draw(T * surface(reverse(plane_hole) ^^ plane_path), white);
  draw(T * unitcube, mediumgray);
}

draw(unitcube, gray);

trj.trajectory(T, (0, 0, 0));
trj.trajectory(T, (0, 1, 0));
trj.trajectory(T, (1, 1, 0));
trj.trajectory(T, (0, 0, 1));
