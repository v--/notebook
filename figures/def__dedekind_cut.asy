usepackage('stix2');
unitsize(1cm);

import graph;

label(Label('$r \leq 2$', align=N), (0.5, 2));
draw((-1, 2) -- (2, 2), linecap(0));
label(Label('$r > 2$', align=N), (3.5, 2), gray);
draw((2, 2) -- (5, 2), gray + linecap(0));
label((2, 2), Label('$2$', align=N));
dot((2, 2));

label(Label('$r < 2$', align=N), (0.5, 1));
draw((-1, 1) -- (2, 1), linecap(0));
label(Label('$r \geq 2$', align=N), (3.5, 1), gray);
draw((2, 1) -- (5, 1), gray + linecap(0));
label((2, 1), Label('$2$', align=N), gray);
dot((2, 1), gray);

label(Label('$r^2 < 2$', align=N), ((-1 + sqrt(2)) / 2, 0));
draw((-1, 0) -- (sqrt(2), 0), linecap(0));
label(Label('$r^2 > 2$', align=N), ((sqrt(2) + 5) / 2, 0), gray);
draw((sqrt(2), 0) -- (5, 0), gray + linecap(0));
