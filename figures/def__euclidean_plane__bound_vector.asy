settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

pair P = (0, -1);
pair Q = (3, 0);
pair R = (-2, 0.5);

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
