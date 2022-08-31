void trajectory(transform T, pair P, pen p = currentpen) {
  dot(P, linewidth(2));
  draw(P -- T * P, arrow=Arrow(TeXHead));
}

void trajectory(transform T(real), real t_0, real t_1, pair P, pen p = currentpen) {
  import graph;
  dot(P, linewidth(2));

  pair f(real angle) {
    return T(angle) * P;
  }

  draw(graph(f, t_0, t_1), arrow=Arrow(TeXHead));
}

void trajectory(transform3 T, triple P) {
  import three;

  dot(P, linewidth(2));
  draw(P -- T * P, arrow=Arrow3(TeXHead2()));
}

void trajectory(transform3 T(real), real t_0, real t_1, triple P, pen p = currentpen) {
  import three;
  import graph3;

  dot(P, linewidth(2));

  triple f(real angle) {
    return T(angle) * P;
  }

  draw(graph(f, t_0, t_1), arrow=Arrow3(TeXHead2()));
}
