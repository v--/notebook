settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = perspective(camera=(-0.2, 0.1, 0.1));

triple o = (-0.1, -0.1, -0.1);
transform3 f = {
  {-1, 0, 0, 2o.x},
  {0, -1, 0, 2o.y},
  {0, 0, -1, 2o.z},
  {0, 0, 0, 1}
};

draw(-1.5X -- 1.5X, gray);
draw(-2Y -- 2Y, gray);
draw(-1.5Z -- 1.5Z, gray);
dot(o, black);

draw(f * unitcube, white);
draw(unitcube, gray);
