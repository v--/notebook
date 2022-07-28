settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair P = (-1, 0);
pair Q = (2, 2);

path l = (-2, -2 / 3) -- (3, 8 / 3);
path g = (-3, 0) -- (4, 0);
path h = (-3, 2) -- (4, 2);

draw(l, L=Label('$l$'));
draw(g, L=Label('$g$', position=0.1));
draw(h, L=Label('$h$', position=0.1));
dot(P, L=Label('$P$', align=S));
dot(Q, L=Label('$Q$', align=N));

draw(arc(P, r=0.3, angle1=0, angle2=32));
draw(arc(Q, r=0.3, angle1=180, angle2=212));
