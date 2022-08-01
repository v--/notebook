settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair P = (-1, 0);
pair Q = (2, 2);
pair R = (P + Q) / 2;
pair G = (R.x, P.y);
pair H = (R.x, Q.y);

path l = (-2, -2 / 3) -- (3, 8 / 3);
path g = (-3, 0) -- (4, 0);
path h = (-3, 2) -- (4, 2);

draw(l, L=Label('$l$', position=0.6));
draw(g, L=Label('$g$', position=0.1, align=N));
draw(h, L=Label('$h$', position=0.1, align=N));
draw(G -- H, dotted);
dot(P, L=Label('$P$', align=S));
dot(G, L=Label('$G$', align=S));
dot(2P - G, L=Label('$G\'$', align=S));
dot(Q, L=Label('$Q$', align=N));
dot(H, L=Label('$H$', align=N));
dot(R, L=Label('$R$', align=NW));

draw(
  arc(
    P,
    r=0.6,
    angle1=0,
    angle2=degrees(atan2((Q - P).y, (Q - P).x))
  ),
  arrow=Arrow(TeXHead)
);

draw(
  arc(
    P,
    r=0.6,
    angle1=180,
    angle2=180 + degrees(atan2((Q - P).y, (Q - P).x))
  ),
  arrow=Arrow(TeXHead)
);

draw(
  arc(
    Q,
    r=0.6,
    angle1=180,
    angle2=180 + degrees(atan2((Q - P).y, (Q - P).x))
  ),
  arrow=Arrow(TeXHead)
);
