settings.outformat = 'pdf';

usepackage('stix2');
unitsize(1cm);

import patterns;

path l = (0, -1) -- (3, 0);
draw(l);

add('left', hatch(1mm));
fill(l -- (3, 0.5) -- (0, 0.5) -- cycle, pattern('left'));
label(Label('$H^-$', position=EndPoint), align=SE, l);

add('right', hatch(1mm, NW));
fill(l -- (3, -1.5) -- (0, -1.5) -- cycle, pattern('right'));
label(Label('$H^+$', position=BeginPoint), align=NW, l);
