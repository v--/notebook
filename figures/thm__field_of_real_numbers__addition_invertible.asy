unitsize(1cm);

import roundedpath;

for (int i = -8; i <= 8; ++i) {
  dot((i / 2, 0), linewidth(2));
}

draw(
  brace((0, 0), (-0.5, 0), -0.1),
  L=Label('$q/2$', align=N/2),
  fontsize(8)
);

draw((-4, 0) -- (4, 0));
dot((0, 0),   L=Label('$0$', align=S));
dot((-1, 0),  L=Label('$q$', align=S));
dot((2, 0), L=Label('$-2q$', align=S));
dot((3, 0), L=Label('$-3q$', align=S));

draw(
  roundedpath((-4, 0.5) -- (2.5, 0.5) -- (2.5, 0), 0.2),
  L=Label('$A$', align=N)
);

newpage();

for (int i = -8; i <= 8; ++i) {
  dot((i / 2, 0), linewidth(2));
}

draw(
  brace((0, 0), (-0.5, 0), -0.1),
  L=Label('$q/2$', align=N),
  fontsize(8)
);

draw((-4, 0) -- (4, 0));
dot((0, 0), L=Label('$0$', align=S));
dot((-1, 0), L=Label('$q$', align=S));
dot((-2, 0), L=Label('$2q$', align=S));
dot((-3, 0), L=Label('$3q$', align=S));

draw(
  roundedpath((-4, 0.5) -- (-2.5, 0.5) -- (-2.5, 0), 0.2),
  L=Label('$A$', align=N)
);
