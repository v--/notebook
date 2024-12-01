unitsize(1.5cm);

import roundedpath;

draw((0, 0) -- (3, 0));

for (int i = 0; i <= 3; ++i) {
  dot((i, 0), L=Label('$' + string(i) + '$', align=S));
}

draw(
  (0, 0.5) -- (2, 0.5) -- (2, 0)
);

label(
  '$\{ a \in \mathbb{Q} | a \leq 2 \}$',
  (1, 0.25),
  fontsize(8)
);

draw(
  roundedpath((2, 0) -- (2, 0.5) -- (3, 0.5), 0.2)
);

label(
  '$\{ a \in \mathbb{Q} | a > 2 \}$',
  (2.6, 0.25),
  fontsize(8)
);

newpage();

draw((0, 0) -- (3, 0));

for (int i = 0; i <= 3; ++i) {
  dot((i, 0), L=Label('$' + string(i) + '$', align=S));
}

draw(
  roundedpath((0, 0.5) -- (2, 0.5) -- (2, 0), 0.2)
);

label(
  '$\{ a \in \mathbb{Q} | a < 2 \}$',
  (1, 0.25),
  fontsize(8)
);

draw(
  (2, 0) -- (2, 0.5) -- (3, 0.5)
);

label(
  '$\{ a \in \mathbb{Q} | a \geq 2 \}$',
  (2.6, 0.25),
  fontsize(8)
);

newpage();

draw((0, 0) -- (3, 0));

for (int i = 0; i <= 3; ++i) {
  dot((i, 0), L=Label('$' + string(i) + '$', align=S));
}

draw(
  roundedpath((0, 0.5) -- (sqrt(2), 0.5) -- (sqrt(2), 0), 0.2)
);

label(
  '$\{ a \in \mathbb{Q} | a^2 \leq 2 \}$',
  (0.65, 0.25),
  fontsize(8)
);

draw(
  roundedpath((sqrt(2), 0) -- (sqrt(2), 0.5) -- (3, 0.5), 0.2)
);

label(
  '$\{ a \in \mathbb{Q} | a^2 \geq 2 \}$',
  (2.2, 0.25),
  fontsize(8)
);
