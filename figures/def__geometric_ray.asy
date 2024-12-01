unitsize(1cm);

path op = (1.5, -0.5) -- (0, -1);
path om = (1.5, -0.5) -- (3, 0);
path pp = (1.5, -1.5) -- (3, -1);
pair O = point(op, 0);
pair P = point(pp, 0);

draw(op, arrow=Arrow(TeXHead), L=Label('$r(-t)$', position=EndPoint), align=W);
draw(om, arrow=Arrow(TeXHead), L=Label('$r(t)$', position=EndPoint), align=E);
draw(pp, arrow=Arrow(TeXHead), L=Label('$s(t)$', position=EndPoint), align=E);
dot(O, L=Label('$O$', position=MidPoint), align=N);
dot(P, L=Label('$P$', position=MidPoint), align=N);
