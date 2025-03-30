unitsize(1.5cm);

import graph;

from notebook access plt, pens;

typedef pair plotter(real);
plotter f_n(int n) {
  return new pair(real t) {
    pair p = (cos(t), sin(t));
    real norm = (abs(p.x) ** n + abs(p.y) ** n) ** (1 / n);
    return p / norm;
  };
}

draw(graph(f_n(1), 0, 2pi), opacity(0.2));
draw(graph(f_n(2), 0, 2pi), opacity(0.4));
draw(graph(f_n(5), 0, 2pi, 1000), opacity(0.6));
draw(graph(f_n(1000), 0, 2pi, 1000));

xaxis(
  arrow=Arrow(TeXHead),
  above=true,
  xmin=-1.5,
  xmax=1.5
);

yaxis(
  arrow=Arrow(TeXHead),
  above=true,
  ymin=-1.5,
  ymax=1.5
);

newpage();
