settings.outformat = 'pdf';
settings.prc = false;
settings.render = 0;

usepackage('stix2');
unitsize(1cm);

import three;

currentprojection = orthographic(camera=(6, -6, 2));

triple A = (1, 0, 3);
triple B = (2, 2, 3);
triple C = (-1, 1, 3);

pen affine_hull = white + opacity(0.4);
pen conic_hull = gray + opacity(0.3);
pen conic_hull_border = darkgray + opacity(0.3);
pen convex_hull = black + opacity(0.2);
pen convex_hull_border = black + opacity(0.2);

draw(A -- B -- C -- cycle, convex_hull_border);
draw(surface(A -- B -- C -- cycle), convex_hull);
draw(O -- 1.5A, conic_hull_border);
draw(O -- 1.5B, conic_hull_border);
draw(O -- 1.5C, conic_hull_border);
draw(surface(O -- 1A -- 1B -- cycle), conic_hull);
draw(surface(O -- 1A -- 1C -- cycle), conic_hull);
draw(surface(O -- 1B -- 1C -- cycle), conic_hull);
draw(surface(plane(8 X, 8 Y, O=(-3, -3, 3))), affine_hull);
draw(surface(B -- A -- 1.5A -- 1.5B -- cycle), conic_hull);
draw(surface(C -- A -- 1.5A -- 1.5C -- cycle), conic_hull);
draw(surface(C -- B -- 1.5B -- 1.5C -- cycle), conic_hull);

label(Label('affine hull'), (3.5, 3, 2.1));
label(Label('convex hull'), (0, 2.5, 3.2));
label(Label('conic hull'), (2.3, 0, 1));

dot(O, L=Label('$\overrightarrow 0$', align=S));
dot(A, L=Label('$A$', align=E));
dot(B, L=Label('$B$', align=E));
dot(C, L=Label('$C$', align=W));
