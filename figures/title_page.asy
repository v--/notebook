usepackage('stix2');

import 'asymptote/random.asy' as random;

real width = 21cm;
real height = -29.7cm;

path boundary = (0, 0) -- (width, 0) -- (width, height) -- (0, height) -- cycle;
pen very_light_gray = rgb(29 / 30, 29 / 30, 29 / 30);
pen moderately_light_gray = rgb(28 / 30, 28 / 30, 28 / 30);

CongGenerator gen = CongGenerator();

void recurse(pair A, pair B, pair C, int depth) {
  if (depth == 0) {
    real test_value = gen.next();

    filldraw(
      A -- B -- C -- cycle,
      fillpen=test_value > 2 / 3 ? very_light_gray : test_value > 1 / 3 ? moderately_light_gray : white,
      drawpen=lightgray
    );

    return;
  }

  recurse(
    A,
    (A + B) / 2,
    (A + C) / 2,
    depth - 1
  );

  recurse(
    (A + B) / 2,
    B,
    (B + C) / 2,
    depth - 1
  );

  recurse(
    (A + C) / 2,
    (B + C) / 2,
    C,
    depth - 1
  );

  recurse(
    (A + C) / 2,
    (B + C) / 2,
    (A + B) / 2,
    depth - 1
  );
}

recurse(
  A=(width, -sqrt(3) * width),
  B=(0, 0),
  C=(2 * width, 0),
  depth=6
);

clip(g=boundary);
