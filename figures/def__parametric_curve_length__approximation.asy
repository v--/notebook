import graph;

settings.outformat = 'pdf';

usepackage('stix2');
unitsize(5cm);

real y(real x) {
  if (x < 1 / 3) {
    return -sqrt(1 - (2 * x * 4 / 3 - 1) ** 2) / 2;
  }

  return -sqrt(1 - (x * 4 / 3 - 1 / 3) ** 2) / 2;
}

// Rational numbers
real[] points_x = { 0, 1 / 4, 2 / 3, 1 };
pair[] points;
path l;

for (real x: points_x) {
  pair p = (x, y(x));
  dot(p);

  points.push(p);
  l = l -- p;
}

label('$\\gamma(0)$', points[0], align=W);
label('$\\gamma \\left( \\frac 1 4 \\right)$', points[1], align=S);
label('$\\gamma \\left( \\frac 2 3 \\right)$', points[2], align=S);
label('$\\gamma(1)$', points[3], align=E);

draw(graph(y, 0, 1));
draw(l);
