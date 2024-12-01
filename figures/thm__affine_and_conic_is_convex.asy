unitsize(1cm);

import three;

currentprojection = orthographic(camera=(6, -6, 2));

triple P = (1, 0, 3);
triple Q = (2, 2, 3);
triple R = (-1, 1, 3);

pen affine_hull = white + opacity(0.4);
pen conic_hull = gray + opacity(0.3);
pen conic_hull_border = darkgray + opacity(0.3);
pen convex_hull = black + opacity(0.2);
pen convex_hull_border = black + opacity(0.2);

draw(P -- Q -- R -- cycle, convex_hull_border);
draw(surface(P -- Q -- R -- cycle), convex_hull);
draw(O -- 1.5P, conic_hull_border);
draw(O -- 1.5Q, conic_hull_border);
draw(O -- 1.5R, conic_hull_border);
draw(surface(O -- Q -- R -- cycle), conic_hull);
draw(surface(O -- P -- R -- cycle), conic_hull);
draw(surface(O -- P -- Q -- cycle), conic_hull);
draw(surface(plane(8 X, 8 Y, O=(-3, -3, 3))), affine_hull);
draw(surface(R -- Q -- 1.5Q -- 1.5R -- cycle), conic_hull);
draw(surface(R -- P -- 1.5P -- 1.5R -- cycle), conic_hull);
draw(surface(Q -- P -- 1.5P -- 1.5Q -- cycle), conic_hull);

label(Label('affine hull'), (3.5, 3, 2.1));
label(Label('convex hull'), (0.2, 3, 3.4));
label(Label('conic hull'), (2.3, 0, 1));

dot(O, L=Label('$O$', align=S));
dot(P, L=Label('$P$', align=NE));
dot(Q, L=Label('$Q$', align=NE));
dot(R, L=Label('$R$', align=NW));
