settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = orthographic(camera=(6, -6, 2));

triple x = (1, 0, 3);
triple y = (2, 2, 3);
triple z = (-1, 1, 3);

pen affine_hull = white + opacity(0.4);
pen conic_hull = gray + opacity(0.3);
pen conic_hull_border = darkgray + opacity(0.3);
pen convex_hull = black + opacity(0.2);
pen convex_hull_border = black + opacity(0.2);

draw(x -- y -- z -- cycle, convex_hull_border);
draw(surface(x -- y -- z -- cycle), convex_hull);
draw(O -- 1.5x, conic_hull_border);
draw(O -- 1.5y, conic_hull_border);
draw(O -- 1.5z, conic_hull_border);
draw(surface(O -- x -- y -- cycle), conic_hull);
draw(surface(O -- x -- z -- cycle), conic_hull);
draw(surface(O -- y -- z -- cycle), conic_hull);
draw(surface(plane(8 X, 8 Y, O=(-3, -3, 3))), affine_hull);
draw(surface(y -- x -- 1.5x -- 1.5y -- cycle), conic_hull);
draw(surface(z -- x -- 1.5x -- 1.5z -- cycle), conic_hull);
draw(surface(z -- y -- 1.5y -- 1.5z -- cycle), conic_hull);

label(Label('affine hull'), (3.5, 3, 2.1));
label(Label('convex hull'), (0, 2.5, 3.2));
label(Label('conic hull'), (2.3, 0, 1));

dot(O, L=Label('$O$', align=S));
dot(x, L=Label('$x$', align=E));
dot(y, L=Label('$y$', align=E));
dot(z, L=Label('$z$', align=W));
