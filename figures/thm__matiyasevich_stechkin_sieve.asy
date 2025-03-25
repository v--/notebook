unitsize(0.5cm);

import graph;

from notebook access plt, pens;

pair f(real t) {
  return (t, t ** 2);
}

int xlim = 4;
int ylim = xlim ** 2;
int xlim_ = floor(ylim / 2);
draw(graph(f, -xlim_, xlim_), pens.thin);

for (int n = 1; n <= xlim_; ++n) {
  pair point_left = (-n, n ** 2);
  dot(point_left);

  if (n == 1) {
    continue;
  }

  for (int m = 2; m < xlim_; ++m) {
    pair point_right = (m, m ** 2);
    draw(point_left -- point_right, dotted + gray);
  }
}

for (int n = 1; n <= xlim_; ++n) {
  pair point_right = (n, n ** 2);
  dot(point_right);

  if (n == 1) {
    continue;
  }

  for (int m = 2; m < xlim_; ++m) {
    pair point_left = (-m, m ** 2);
    draw(point_left -- point_right, dotted + gray);

    pair point_ordinate = (0, n * m);
    dot(point_ordinate);
    label(point_ordinate, string(n * m), align=E);
  }
}

xaxis(
  arrow=Arrow(TeXHead),
  above=true
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true
);

for (int n = -xlim; n <= xlim; ++n) {
  pair point_abscissa = (n, 0);
  dot(point_abscissa);
  label(point_abscissa, string(-n), align=S);

  pair point_parabola = (n, n ** 2);
  draw(point_abscissa -- point_parabola, dotted);
}

for (int n = 2; n < xlim ** 2; ++n) {
  bool is_prime = true;

  if (n > 3) {
    for (int m = 2; m < xlim; ++m) {
      if (n % m == 0) {
        is_prime = false;
      }
    }
  }

  if (is_prime) {
    pair point_ordinate = (0, n);
    dot(point_ordinate);
    label(point_ordinate, string(n), align=W);
  }
}

limits(min=(-xlim - 1, -2.5), max=(+xlim + 1, ylim + 1), crop=Crop);
