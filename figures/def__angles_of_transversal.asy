usepackage('stix2');
unitsize(1cm);

import geometry;
import 'asymptote/angles.asy' as angles;

pair refl(pair A, pair O, real coeff = 1/2) {
  return O - coeff * (A - O);
}

// Extender coefficient
real e = 0.8;

path g = (-4, 0) -- (4, 0);
path h = (-4, 2.5) -- (4, 2);

pair P = point(g, 0.3);
pair Q = point(h, 0.7);

pair Pp = orth_proj(P, point(h, 0), point(h, 1) - point(h, 0));
pair Qp = orth_proj(Q, point(g, 0), point(g, 1) - point(g, 0));

path l = refl(P, Q, e) -- refl(Q, P, e);

draw(l, L=Label('$l$', position=0.5), dotted);
draw(point(l, 0) -- refl(P, Q));
draw(P -- Q);
draw(refl(Q, P) -- point(l, 1));

draw(g, L=Label('$g$', position=0.02, align=S), dotted);
draw(P -- Qp);
draw(point(g, 1) -- orth_proj(refl(Pp, Q), point(g, 0), point(g, 1) - point(g, 0)));
draw(point(g, 0) -- refl(Qp, P));

draw(h, L=Label('$h$', position=0.02, align=S), dotted);
draw(Q -- Pp);
draw(point(h, 0) -- orth_proj(refl(Qp, P), point(h, 0), point(h, 1) - point(h, 0)));
draw(point(h, 1) -- refl(Pp, Q));

dot(P, L=Label('$P$', align=S));
dot((3P - Q)/2, L=Label("$2P - Q$", align=SE));
dot((3P - Qp)/2, L=Label("$2P - Q'$", align=N));
dot(Pp, L=Label("$P'$", align=N));
dot(Q, L=Label('$Q$', align=N));
dot((3Q - P)/2, L=Label("$2Q - P$", align=NW));
dot((3Q - Pp)/2, L=Label("$2Q - P'$", align=S));
dot(Qp, L=Label("$Q'$", align=S));

markangle(
  Qp, P, Q,
  radius=15,
  arrow=Arrow(TeXHead)
);

markangle(
  Pp, Q, P,
  radius=15,
  arrow=Arrow(TeXHead)
);
