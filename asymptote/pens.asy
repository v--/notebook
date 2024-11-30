import patterns;

add('left_hatch', hatch(1mm));
add('right_hatch', hatch(1mm, NW));

pen densely_dashed = linetype(new real[] { 2, 2 });
pen left_hatch = pattern('left_hatch');
pen right_hatch = pattern('right_hatch');
