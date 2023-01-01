usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/trajectories.asy' as trajectories;

real angle = 4;
pair O = -0.3 * (1, 1);
transform T = (
  2O.x, 2O.y,
  -1, 0,
  0, -1
);

fill(unitsquare, gray);
fill(T * unitsquare, mediumgray);

dot(O);

trajectory(T, (0, 0));
trajectory(T, (1, 0));
trajectory(T, (0, 1));
