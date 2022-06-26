settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = perspective(camera=(1.5, 1, 1.5));

transform3 f = {
  {1, 0, 0, -1},
  {0, 1, 0, 1.5},
  {0, 0, 1, 2},
  {0, 0, 0, 1}
};

draw(-6X -- 2.5X, gray);
draw(-2Y -- 3.5Y, gray);
draw(-2.5Z -- 3Z, gray);

draw(unitcube, gray);
draw(f * unitcube, white);
