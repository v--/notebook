unitsize(1.5cm);

import graph;
from notebook access trj;

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

trj.trajectory(rot, 0, final_angle, (1, 1));
trj.trajectory(rot, 0, final_angle, (0, 1));
