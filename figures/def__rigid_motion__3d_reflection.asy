settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = perspective(camera=(-0.2, 0.3, 0.2));

transform3 f = {
  {1 / 3, -2 / 3, -2 / 3, 0},
  {-2 / 3, 1 / 3, -2 / 3, 0},
  {-2 / 3, -2 / 3, 1 / 3, 0},
  {0, 0, 0, 1}
};

draw(f * unitcube, white);

draw(-1.5X -- 1.5X, gray);
draw(-3Y -- 2Y, gray);
draw(-1.5Z -- 1.5Z, gray);

draw(unitcube, gray);
