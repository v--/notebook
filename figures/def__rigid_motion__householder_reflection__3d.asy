settings.outformat = 'pdf';
settings.prc = false;
settings.render = 5;

usepackage('stix2');
unitsize(1.5cm);

import three;

currentprojection = orthographic(camera=(-0.5, 0.5, 0.2));
currentlight = (0.5, 1, 1.25);

transform3 f = {
  {1, 0, 0, 0},
  {0, 0, -1, 0},
  {0, -1, 0, 0},
  {0, 0, 0, 1}
};

void trajectory(triple p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow3(TeXHead2()));
}

draw(f * unitcube, white);
draw(unitcube, gray);
draw(surface((-1, 1, -1) --- (2, 1, -1) --- (2, -1, 1) --- (-1, -1, 1) --- cycle), gray + opacity(0.5));

trajectory((1, 1, 0));
trajectory((0, 1, 0));
trajectory((0, 0, 1));
trajectory((0, 1, 1));
