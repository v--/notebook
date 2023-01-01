usepackage('stix2');
unitsize(1.5cm);

import three;
import 'asymptote/trajectories.asy' as trajectories;

currentprojection = perspective(camera=(-0.5, -2, 1.5));
currentlight = (-1, -0.5, 5);

real final_angle_f = -pi/2;
real final_angle_g = 2.5;

transform3 rot(real factor) {
  real angle_f = factor * final_angle_f;
  real angle_g = factor * final_angle_g;

  transform3 g = {
    {cos(angle_g), -sin(angle_g), 0, 0},
    {sin(angle_g), cos(angle_g), 0, 0},
    {0, 0, 1, 0},
    {0, 0, 0, 1}
  };

  transform3 f = {
    {1, 0, 0, 0},
    {0, cos(angle_f), -sin(angle_f), 0},
    {0, sin(angle_f), cos(angle_f), 0},
    {0, 0, 0, 1}
  };

  return g * f;
};

draw(unitcube, gray + opacity(0.75));
draw(rot(1) * unitcube, white + opacity(0.75));

dot((0, 0, 0), linewidth(2));
trajectory(rot, 0, 1, (0, 0, 1));
trajectory(rot, 0, 1, (1, 0, 1));
trajectory(rot, 0, 1, (1, 0, 0));
