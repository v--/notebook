settings.outformat = 'pdf';
import patterns;

usepackage('stix2');
defaultpen(fontsize(10pt));

path l = (0, -1cm) -- (3cm, 0);
draw(l);

add('left', hatch(1mm));
fill(l -- (3cm, 0.5cm) -- (0, 0.5cm) -- cycle, pattern('left'));
label(Label('$H^-$', position=EndPoint), align=SE, l);

add('right', hatch(1mm, NW));
fill(l -- (3cm, -1.5cm) -- (0, -1.5cm) -- cycle, pattern('right'));
label(Label('$H^+$', position=BeginPoint), align=NW, l);
