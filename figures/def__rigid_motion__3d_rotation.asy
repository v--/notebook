settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = perspective(camera=(-0.5, -3, 1.5));

transform3 f = {
  {cos(2), -sin(2), 0, 0},
  {sin(2), cos(2), 0, 0},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};

transform3 g = {
  {1, 0, 0, 0},
  {0, cos(-1), -sin(-1), 0},
  {0, sin(-1), cos(-1), 0},
  {0, 0, 0, 1}
};

draw(unitcube, gray);

draw(-1.5X -- 1.5X, gray);
draw(-1.5Y -- 1.5Y, gray);
draw(-1.5Z -- 1.5Z, gray);

draw(f * g * unitcube, white);
