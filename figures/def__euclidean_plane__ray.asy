settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

path rp = (1.5, -0.5) -- (0, -1);
path rm = (1.5, -0.5) -- (3, 0);
path sp = (1.5, -1.5) -- (3, -1);
pair R = point(rp, 0);
pair S = point(sp, 0);

draw(rp, arrow=Arrow(TeXHead), L=Label('$r^-$', position=EndPoint), align=W);
draw(rm, arrow=Arrow(TeXHead), L=Label('$r^+$', position=EndPoint), align=E);
draw(sp, arrow=Arrow(TeXHead), L=Label('$s^+$', position=EndPoint), align=E);
dot(R, L=Label('$R$', position=MidPoint), align=N);
dot(S, L=Label('$S$', position=MidPoint), align=N);
