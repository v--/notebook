settings.outformat = 'pdf';

usepackage('stix2');
defaultpen(fontsize(10pt));

pair P = (0, -1cm);
pair Q = (3cm, 0);
pair R = (-2cm, 0.5cm);

path PQ = P -- Q;
path PR = P -- R;

draw(PQ, arrow=Arrow(TeXHead));
label(Label('$\overrightarrow{PQ}$', position=MidPoint), align=SE, PQ);

draw(PR, arrow=Arrow(TeXHead));
label(Label('$\overrightarrow{PR}$', position=MidPoint), align=SW, PR);

dot(P);
label(Label('$P$', position=MidPoint), align=S, P);
label(Label('$Q$', position=MidPoint), align=S, Q);
label(Label('$R$', position=MidPoint), align=SW, R);
