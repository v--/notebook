settings.outformat = 'pdf';
settings.prc = false;
settings.render = 5;

usepackage('stix2');
unitsize(1.5cm);

import three;

currentprojection = orthographic(camera=(-0.2, 0.1, 0.1));

triple o = -0.2 * (1, 1, 1);
transform3 f = {
  {-1, 0, 0, 2o.x},
  {0, -1, 0, 2o.y},
  {0, 0, -1, 2o.z},
  {0, 0, 0, 1}
};

void trajectory(triple p) {
  dot(p, linewidth(2));
  draw(p -- f * p, arrow=Arrow3(TeXHead2()));
}

draw(f * unitcube, white);
draw(unitcube, gray);

dot(o);
trajectory((0, 0, 0));
trajectory((0, 1, 0));
trajectory((0, 0, 1));
