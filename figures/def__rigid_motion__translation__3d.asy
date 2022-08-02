settings.outformat = 'pdf';
settings.prc = false;
settings.render = 5;

usepackage('stix2');
unitsize(1.5cm);

import three;

currentprojection = orthographic(camera=(2, 0.5, 1));

transform3 f = {
  {1, 0, 0, -1},
  {0, 1, 0, -1.5},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};

void trajectory(triple p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow3(TeXHead2()));
}

draw(f * unitcube, white);
draw(unitcube, gray);

trajectory((1, 0, 0));
trajectory((1, 0, 1));
trajectory((0, 0, 1));
trajectory((0, 1, 1));
