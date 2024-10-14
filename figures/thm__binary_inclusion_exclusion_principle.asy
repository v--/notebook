usepackage('stix2');
unitsize(1cm);

pair A = (0, 0);
pair U = (4, 0);
pair B = (8, 0);

draw(shift(A) * unitcircle);
draw(A + (-1, 0) -- A + (1, 0));
label(A + (0, 0.5), '$A \setminus B$');
label(A + (0, -0.5), '$A \cap B$');
label(A + (0, -1), '$A$', align=2S);

draw(
  A + (2, 1) / sqrt(5) -- U + (-2, 1) / sqrt(5),
  arrow=Arrow(TeXHead)
);

draw(
  A + (2, -1) / sqrt(5) .. U + (-2, 1) / sqrt(5) - (0.1, 0) .. U + (-2, 1) / sqrt(5)
);

label('$f_a$', (A + U) / 2, align=S);

draw(shift(U) * unitcircle);
draw(U + (-1, 0) -- U + (1, 0));
label(U + (0, 0.5), '$A \cup B$');
label(U + (0, -0.5), '$A \cap B$');
label(U + (0, -1), '$U$', align=2S);

draw(
  B + (-2, 1) / sqrt(5) -- U + (2, 1) / sqrt(5),
  arrow=Arrow(TeXHead)
);

draw(
  B + (-2, -1) / sqrt(5) -- U + (2, -1) / sqrt(5),
  arrow=Arrow(TeXHead)
);

label('$f_b$', (U + B) / 2);

draw(shift(B) * unitcircle);
draw(B + (-1, 0) -- B + (1, 0));
label(B + (0, 0.5), '$B \setminus A$');
label(B + (0, -0.5), '$A \cap B$');
label(B + (0, -1), '$B$', align=2S);
