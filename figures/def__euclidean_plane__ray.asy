settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

path rp = (1.5, -0.5) -- (0, -1);
path rm = (1.5, -0.5) -- (3, 0);
path sp = (1.5, -1.5) -- (3, -1);
pair R = point(rp, 0);
pair S = point(sp, 0);

draw(rp, arrow=Arrow(TeXHead));
label(Label('$r^-$', position=EndPoint), align=W, rp);

draw(rm, arrow=Arrow(TeXHead));
label(Label('$r^+$', position=EndPoint), align=E, rm);

dot(R);
label(Label('$R$', position=MidPoint), align=N, R);

draw(sp, arrow=Arrow(TeXHead));
label(Label('$s^+$', position=EndPoint), align=E, sp);

dot(S);
label(Label('$S$', position=MidPoint), align=N, S);
