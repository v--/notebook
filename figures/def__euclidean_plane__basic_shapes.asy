settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

path l = (0, -1) -- (3, 0);
path h = (0, -2) -- (3, -1);
path g = (0, 0) -- (3, -2);

pair P = point(g, 0.2);
pair Q = point(g, 0.8);
pair R = point(g, 0.4);

draw(l, L=Label('l', position=MidPoint), align=N);
draw(h, L=Label('h', position=MidPoint));
draw(g, L=Label('g', position=MidPoint), align=NE);
dot(P, L=Label('P'), align=SW);
dot(Q, L=Label('Q'), align=SW);
dot(R, L=Label('R'), align=SW);
