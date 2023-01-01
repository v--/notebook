usepackage('stix2');
unitsize(1.5cm);

import three;
import 'asymptote/trajectories.asy' as trajectories;

currentprojection = orthographic(camera=(2, 0.5, 1));

transform3 T = {
  {1, 0, 0, -1},
  {0, 1, 0, -1.5},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};

draw(T * unitcube, white);
draw(unitcube, gray);

trajectory(T, (1, 0, 0));
trajectory(T, (1, 0, 1));
trajectory(T, (0, 0, 1));
trajectory(T, (0, 1, 1));
