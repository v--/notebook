unitsize(1.5cm);

from notebook access trj;

pair O = -1 / 10 * (1, 1);
pair v = sqrt(2) / 2 * (1, 1);

transform f = (
  0, 0,
  2 * v.x * v.x, 2 * v.y * v.x,
  2 * v.x * v.y, 2 * v.y * v.y
);

transform T = (
  f.xx * O.x + f.xy * O.y, f.yx * O.x + f.yy * O.y,
  1 - f.xx,   - f.yx,
    - f.xy, 1 - f.yy
);

fill(unitsquare, gray);
fill(T * unitsquare, mediumgray);
draw((O.x + v.y, O.y - v.x) -- (O.x - v.y, O.y + v.x), gray + dashed);

trj.trajectory(T, (0, 0));
trj.trajectory(T, (1, 0));
trj.trajectory(T, (0, 1));
