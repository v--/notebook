settings.outformat = 'pdf';

usepackage('stix2');
unitsize(0.5cm);

path l = (0, -1) -- (3, 0);
path h = (0, -2) -- (3, -1);
path g = (0, 0) -- (3, -2);

pair P = point(g, 0.2);
pair Q = point(g, 0.8);
pair R = point(g, 0.4);

draw(l);
label(Label('l', position=MidPoint), align=N, l);

draw(h);
label(Label('h', position=MidPoint), h);

draw(g);
label(Label('g', position=MidPoint), align=NE, g);

dot(P);
label(Label('P'), align=SW, P);

dot(Q);
label(Label('Q'), align=SW, Q);

dot(R);
label(Label('R'), align=SW, R);
