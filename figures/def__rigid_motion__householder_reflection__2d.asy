settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

pair O = -1 / 10 * (1, 1);
pair v = sqrt(2) / 2 * (1, 1);

transform g = (
  0, 0,
  2 * v.x * v.x, 2 * v.y * v.x,
  2 * v.x * v.y, 2 * v.y * v.y
);

transform f = (
  g.xx * O.x + g.xy * O.y, g.yx * O.x + g.yy * O.y,
  1 - g.xx,   - g.yx,
    - g.xy, 1 - g.yy
);

void trajectory(pair p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow(TeXHead));
}

fill(unitsquare, gray);
fill(f * unitsquare, mediumgray);
draw((O.x + v.y, O.y - v.x) -- (O.x - v.y, O.y + v.x), gray + dashed);

trajectory((0, 0));
trajectory((1, 0));
trajectory((0, 1));
