usepackage('stix2');
unitsize(1.5cm);

import graph;

real final_angle = 2.5;

pair phi(pair p, real t) {
  return (
    p.x * cos(t) - p.y * sin(t),
    p.x * sin(t) + p.y * cos(t)
  );
}

typedef pair mover(real);
mover phi_partial(pair p) {
  return new pair(real t) {
    return phi(p, t);
  };
}

{
  pair p1 = phi((1, 0), pi / 8);

  dot(p1);
  label(Label('$P_1$', p1, align=E));

  draw(
    graph(phi_partial(p1), 0, pi / 4),
    arrow=Arrow(TeXHead)
  );

  label(Label('Rotate $P_1$ by $\pi / 4$'), phi(p1, pi / 8), align=NE);
}

{
  pair p2 = phi((0, -1), -pi / 8);

  dot(p2);
  label(Label('$P_2$', p2, align=E));

  draw(
    graph(phi_partial(p2), 0, -pi / 2),
    arrow=Arrow(TeXHead)
  );

  label(Label('Rotate $P_2$ by $-\pi / 2$'), phi(p2, -pi / 4), align=SW);
}

xaxis(
  arrow=Arrow(TeXHead),
  dashed,
  above=true,
  xmin=-3.5,
  xmax=3.5
);

yaxis(
  arrow=Arrow(TeXHead),
  dashed,
  above=true,
  ymin=-1.5,
  ymax=1.5
);
