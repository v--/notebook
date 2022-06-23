settings.outformat = 'pdf';

usepackage('stix2');
defaultpen(fontsize(10pt));

path rp = (1.5cm, -0.5cm) -- (0, -1cm);
path rm = (1.5cm, -0.5cm) -- (3cm, 0);
path sp = (1.5cm, -1.5cm) -- (3cm, -1cm);
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
