settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = perspective(camera=(-0.5, -3, 1.5));

real angle_f = 2;
transform3 f = {
  {cos(angle_f), -sin(angle_f), 0, 0},
  {sin(angle_f), cos(angle_f), 0, 0},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};

real angle_g = -1;
transform3 g = {
  {1, 0, 0, 0},
  {0, cos(angle_g), -sin(angle_g), 0},
  {0, sin(angle_g), cos(angle_g), 0},
  {0, 0, 0, 1}
};

draw(unitcube, gray);

draw(-1.5X -- 1.5X, gray);
draw(-1.5Y -- 1.5Y, gray);
draw(-1.5Z -- 1.5Z, gray);

draw(f * g * unitcube, white);
