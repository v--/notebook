settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import 'asy/trajectories.asy' as trajectories;

transform T = (
  1.5, 0.5,
  1, 0,
  0, 1
);

fill(unitsquare, gray);
fill(T * unitsquare, mediumgray);

trajectory(T, (0, 0));
trajectory(T, (1, 0));
trajectory(T, (0, 1));
trajectory(T, (1, 1));
