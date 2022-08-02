settings.outformat = 'pdf';
settings.prc = false;
settings.render = 5;

usepackage('stix2');
unitsize(2cm);

import three;

currentprojection = orthographic(camera=(-0.2, 0.3, 0.2));

transform3 f = {
  {1, 0, 0, 0},
  {0, 4 / 5, -2 / 5, -1 / 5},
  {0, -2 / 5, 1 / 5, -2 / 5},
  {0, 0, 0, 1}
};

void trajectory(triple p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow3(TeXHead2()));
}

draw(f * unitcube, mediumgray);
draw(unitcube, gray);
draw(surface(f * (-1 / 2, -1, 0) -- f * (-1 / 2, 3 / 2, 0) -- f * (3 / 2, 3 / 2, 0) -- f * (3 / 2, -1, 0) -- cycle), white);

trajectory((0, 0, 0));
trajectory((1, 0, 0));
trajectory((0, 1, 0));
trajectory((1, 1, 0));
trajectory((0, 0, 1));
