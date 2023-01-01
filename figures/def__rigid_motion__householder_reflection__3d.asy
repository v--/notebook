usepackage('stix2');
unitsize(1.5cm);

import three;
import 'asymptote/trajectories.asy' as trajectories;

currentprojection = orthographic(camera=(-0.5, 0.5, 0.2));
currentlight = (0.5, 1, 1.25);

transform3 T = {
  {1, 0, 0, 0},
  {0, 0, -1, 0},
  {0, -1, 0, 0},
  {0, 0, 0, 1}
};

draw(T * unitcube, white);
draw(surface((-1, 1, -1) --- (2, 1, -1) --- (2, -1, 1) --- (-1, -1, 1) --- cycle), gray + opacity(0.5));
draw(unitcube, gray);

trajectory(T, (1, 1, 0));
trajectory(T, (0, 1, 0));
trajectory(T, (0, 0, 1));
trajectory(T, (0, 1, 1));
