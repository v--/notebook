usepackage('stix2');
unitsize(1cm);

import roundedpath;

pair a = (-1, 0);
pair b = (0, 0);
pair c = (1, 0);
pair d = (0, 1);

pair TN = N / 10;
pair TE = E / 10;
pair TS = S / 10;
pair TW = W / 10;

draw(
  b + 1.5 * (TN + TW) --
  c + 1.5 * (TN + TE) --
  c + 1.5 * (TS + TE) --
  b + 1.5 * (TS + TW) --
  cycle,
  gray
);

label(Label('$A$', align=E), c + 2 * TE);

draw(
  d + 2 * (TN + TW) --
  d + 2 * (TN + TE) --
  d + 2 * (TS + TE) --
  d + 2 * (TS + TW) --
  cycle,
  gray
);

label(Label('$A^U$', align=E), d + 2 * TE);

draw(
  a + 2.5 * (TN + TW) --
  c + 2.5 * (TN + TE) --
  c + 2.5 * (TS + TE) --
  a + 2.5 * (TS + TW) --
  cycle,
  gray
);

label(Label('$A^{UL}$', align=W), a + 2 * TW);

dot(a, L=Label('$a$', align=2.5 * S));
dot(b, L=Label('$b$', align=2.5 * S));
dot(c, L=Label('$c$', align=2.5 * S));
dot(d, L=Label('$d$', align=2.5 * N));

draw(a + TN + TE -- d + TS + TW);
draw(b + TN -- d + TS);
draw(c + TN + TW -- d + TS + TE);
