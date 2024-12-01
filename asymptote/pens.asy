access patterns;

patterns.add('ne_hatch', patterns.hatch(1, NE, mediumgray));
patterns.add('nw_hatch', patterns.hatch(1, NW, mediumgray));

pen densely_dashed = linetype(new real[] { 2, 2 });
pen ne_hatch = pattern('ne_hatch');
pen pale_ne_hatch = pattern('pale_ne_hatch');
pen nw_hatch = pattern('nw_hatch');
pen thin = linewidth(0.1 * linewidth());
