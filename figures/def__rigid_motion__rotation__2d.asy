settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1.5cm);

import graph;

real final_angle = 2.5;

transform rot(real angle) {
  return (
    0, 0,
    cos(angle), -sin(angle),
    sin(angle), cos(angle)
  );
};

void trajectory(pair p) {
  dot(p, linewidth(2));

  pair f(real angle) {
    return rot(angle) * p;
  }

  draw(graph(f, 0, final_angle), arrow=Arrow(TeXHead));
}

fill(unitsquare, gray);
fill(rot(final_angle) * unitsquare, mediumgray);

trajectory((1, 1));
trajectory((0, 1));
