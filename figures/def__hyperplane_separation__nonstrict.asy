usepackage('stix2');
unitsize(1cm);

path l = (-1.5, -1.5) -- (1.5, 1.5);
draw(l, L=Label('$l$', position=EndPoint, align=S));

draw(shift(-sqrt(2) / 2, sqrt(2) / 2) * unitcircle, L=Label('$A$', align=W));
draw(shift(sqrt(2) / 2, -sqrt(2) / 2) * unitcircle, L=Label('$B$', position=BeginPoint, align=E));
