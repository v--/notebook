settings.outformat = 'pdf';

usepackage('stix2');
defaultpen(fontsize(10pt));

draw(circle((0, 0), 1cm));
draw((-2.5cm, 0) -- (-1.25cm, -0.5cm) -- (-2cm, 1.5cm) -- cycle);
draw((2cm, -0.5cm) -- (-0.5cm, -1.5cm));
