settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

transform f = (
  1.5, 0.5,
  1, 0,
  0, 1
);

void trajectory(pair p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow(TeXHead));
}

fill(unitsquare, gray);
fill(f * unitsquare, mediumgray);

trajectory((0, 0));
trajectory((1, 0));
trajectory((0, 1));
trajectory((1, 1));
