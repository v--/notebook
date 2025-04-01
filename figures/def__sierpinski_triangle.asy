usepackage('stix2');
unitsize(4cm);


void recurse(pair A, pair B, pair C, int depth, bool fill_ = true) {
  if (depth == 0) {
    if (fill_) {
      fill(A -- B -- C -- cycle);
    }

    return;
  }

  recurse(
    A,
    (A + B) / 2,
    (A + C) / 2,
    depth - 1,
    fill_=fill_ && true
  );

  recurse(
    (A + B) / 2,
    B,
    (B + C) / 2,
    depth - 1,
    fill_=fill_ && true
  );

  recurse(
    (A + C) / 2,
    (B + C) / 2,
    C,
    depth - 1,
    fill_=fill_ && true
  );

  recurse(
    (A + C) / 2,
    (B + C) / 2,
    (A + B) / 2,
    depth - 1,
    fill_=false
  );
}


recurse(
  A=(0, 0),
  B=(2, 0),
  C=(1, sqrt(3)),
  depth=5
);
