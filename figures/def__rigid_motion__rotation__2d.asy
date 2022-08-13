settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asy/trajectories.asy' as trajectories;

real final_angle = 2.5;

transform rot(real angle) {
  return (
    0, 0,
    cos(angle), -sin(angle),
    sin(angle), cos(angle)
  );
};

fill(unitsquare, gray);
fill(rot(final_angle) * unitsquare, mediumgray);

trajectory(rot, 0, final_angle, (1, 1));
trajectory(rot, 0, final_angle, (0, 1));
