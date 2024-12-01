unitsize(1cm);

import geometry;

from notebook access geom;

// Reflect around O, but shorten the distance. We use is used for visually shortening distance.
point refl(point A, point O, real coeff = 1 / 2) {
  return O - coeff * (A - O);
}

line g = line((-4, 0), (4, 0));
line h = line((-4, 2.5), (4, 2));

point P = point(g, 0.3);
point Q = point(h, 0.7);

point P_ = projection(h) * P;
point Q_ = projection(g) * Q;

line l = line(P, Q);

line g_start = line(P_, Q, extendB=false);
line g_end =   line(refl(P_, O=Q), refl(P_, O=Q, coeff=1), extendA=false);

line h_start = line(Q_, P, extendB=false);
line h_end =   line(refl(Q_, O=P), refl(Q_, O=P, coeff=1), extendA=false);

line l_start = line(refl(Q, O=P), refl(Q, O=P, coeff=1), extendA=false);
line l_end =   line(refl(P, O=Q), refl(P, O=Q, coeff=1), extendA=false);

draw(l, L=Label('$l$', position=0.5), dotted);
draw(P -- Q);
draw(l_start);
draw(l_end);

draw(g, L=Label('$g$', position=0.98, align=S), dotted);
draw(g_start);
draw(g_end);

draw(h, L=Label('$h$', position=0.02, align=S), dotted);
draw(h_start);
draw(h_end);

dot(P,             L=Label('$P$', align=S));
dot(refl(Q, O=P),  L=Label("$\rho_P(Q)$", align=SE));
dot(refl(Q_, O=P), L=Label("$\rho_P(Q')$", align=N));
dot(P_,            L=Label("$P'$", align=N));
dot(Q,             L=Label('$Q$', align=N));
dot(refl(P, O=Q),  L=Label("$\rho_Q(P)$", align=NW));
dot(refl(P_, O=Q), L=Label("$\rho_Q(P')$", align=S));
dot(Q_,            L=Label("$Q'$", align=S));

geom.mark_angle(
  Q_, P, Q,
  radius=15,
  arrow=Arrow(TeXHead)
);

geom.mark_angle(
  P_, Q, P,
  radius=15,
  arrow=Arrow(TeXHead)
);
