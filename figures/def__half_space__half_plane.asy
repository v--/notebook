usepackage('stix2');
unitsize(1.5cm);

import 'asymptote/pens.asy' as pens;

path l = (0, -1) -- (3, 0);
draw(l);

fill(l -- (3, 0.5) -- (0, 0.5) -- cycle, left_hatch);
label(Label('$H^-$', position=EndPoint), align=SE, l);

fill(l -- (3, -1.5) -- (0, -1.5) -- cycle, right_hatch);
label(Label('$H^+$', position=BeginPoint), align=NW, l);
