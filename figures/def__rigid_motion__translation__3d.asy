unitsize(1.5cm);

import three;
from notebook access trj;

currentprojection = orthographic(camera=(2, 0.5, 1));

transform3 T = {
  {1, 0, 0, -1},
  {0, 1, 0, -1.5},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};

draw(T * unitcube, white);
draw(unitcube, gray);

trj.trajectory(T, (1, 0, 0));
trj.trajectory(T, (1, 0, 1));
trj.trajectory(T, (0, 0, 1));
trj.trajectory(T, (0, 1, 1));
