unitsize(1cm);

pair origin = (0, 0);
pair v = (0.5, 0.5);

draw(circle(origin, 1.5));
dot(origin);
label('$y$', align=S, origin);

pair x1 = -sqrt(2) * v;
draw(circle(x1, 0.5));
dot(x1);
label('$x_1$', align=S, x1);

pair x2 = sqrt(2) / 2 * v;
draw(circle(x2, 0.5));
dot(x2);
label('$x_2$', align=S, x2);
