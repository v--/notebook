settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

real angle = 4;
pair O = -0.3 * (1, 1);
transform f = (
  2O.x, 2O.y,
  -1, 0,
  0, -1
);

void trajectory(pair p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow(TeXHead));
}

fill(unitsquare, gray);
fill(f * unitsquare, mediumgray);

dot(O);

trajectory((0, 0));
trajectory((1, 0));
trajectory((0, 1));
