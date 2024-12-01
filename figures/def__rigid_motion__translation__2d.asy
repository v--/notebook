unitsize(1.5cm);

from notebook access trj;

transform T = (
  1.5, 0.5,
  1, 0,
  0, 1
);

fill(unitsquare, gray);
fill(T * unitsquare, mediumgray);

trj.trajectory(T, (0, 0));
trj.trajectory(T, (1, 0));
trj.trajectory(T, (0, 1));
trj.trajectory(T, (1, 1));
