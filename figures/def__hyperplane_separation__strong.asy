settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

path l = (-1.5, -1) -- (3, 2);
draw(l, L=Label('$l$', position=EndPoint, align=S));

pair n = (-3, 2);

path lp = (-1.5, -1) + n/15 -- (3, 2) + n/15;
draw(lp, L=Label('$l\'$', position=EndPoint, align=NW));

draw(shift(-1, 1) * unitcircle, L=Label('$A$', align=W));
draw(shift(2, 0) * unitcircle, L=Label('$B$', position=BeginPoint, align=E));
