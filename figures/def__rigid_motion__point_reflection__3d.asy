settings.outformat = 'pdf';
settings.prc = false;
settings.render = 5;

usepackage('stix2');
unitsize(1.5cm);

import three;
import 'asy/trajectories.asy' as trajectories;

currentprojection = orthographic(camera=(-0.2, 0.1, 0.1));

triple o = -0.2 * (1, 1, 1);
transform3 T = {
  {-1, 0, 0, 2o.x},
  {0, -1, 0, 2o.y},
  {0, 0, -1, 2o.z},
  {0, 0, 0, 1}
};

draw(T * unitcube, white);
draw(unitcube, gray);

dot(o);
trajectory(T, (0, 0, 0));
trajectory(T, (0, 1, 0));
trajectory(T, (0, 0, 1));
