settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import graph;

pair O = (0, 0);

path g = (-3, -2) -- (3, 2);
path h = (-3, 0) -- (3, 0);

draw(g, L=Label('$g$', position=0.1));
draw(h, L=Label('$h$', position=0.1));
dot(O, L=Label('$O$', align=S));

draw(arc(O, r=0.3, angle1=0, angle2=32));
draw(arc(O, r=0.3, angle1=180, angle2=212));
