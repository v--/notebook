settings.outformat = 'pdf';
settings.prc = false;
settings.render = 5;

usepackage('stix2');
unitsize(2cm);

import three;
import 'asymptote/trajectories.asy' as trajectories;

currentprojection = orthographic(camera=(-0.2, 0.3, 0.2));

transform3 T = {
  {1, 0, 0, 0},
  {0, 4 / 5, -2 / 5, -1 / 5},
  {0, -2 / 5, 1 / 5, -2 / 5},
  {0, 0, 0, 1}
};

draw(T * unitcube, mediumgray);
draw(unitcube, gray);
draw(surface(T * (-1 / 2, -1, 0) -- T * (-1 / 2, 3 / 2, 0) -- T * (3 / 2, 3 / 2, 0) -- T * (3 / 2, -1, 0) -- cycle), white);

trajectory(T, (0, 0, 0));
trajectory(T, (1, 0, 0));
trajectory(T, (0, 1, 0));
trajectory(T, (1, 1, 0));
trajectory(T, (0, 0, 1));
