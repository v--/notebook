usepackage('stix2');
unitsize(1.5cm);

import graph;
import 'asymptote/pens.asy' as pens;
import 'asymptote/polygons.asy' as polygons;

int n = 6;
pair o = (0, 0);
real lim = 1.5;

pair[] vert;
pair[] norm;

for (int k = 0; k < n; ++k) {
  pair v = polar(1, pi / 3 * k);
  vert.push(v);
  pair n = v.x == 0 ? unit((1, -v.x / v.y)) : unit((-v.y / v.x, 1));
  norm.push(n); // Normal to o -- v
}

for (int k = 0; k < 2; ++k) {
  pair m = vert[k] / 2;
  pair d = 4norm[k];
  pair m_ = -4m;
  pen p = k % 2 == 0 ? left_hatch : right_hatch;
  fill(m - d -- m + d -- m_ + d -- m_ - d -- cycle, p + opacity(0.3));
}

dot(o, L=Label('$A$'), align=-(vert[0] + vert[1]));
dot(vert[0], L=Label('$V_1$', align=NE));
dot(vert[1], L=Label('$V_2$', align=NE));
dot(vert[2], L=Label('$V_3$', align=N));
dot(vert[3], L=Label('$V_4$', align=vert[3]));
dot(vert[4], L=Label('$V_5$', align=vert[4]));
dot(vert[5], L=Label('$V_6$', align=SE));
dot(vert[0] / 2, L=Label('$M_1$', align=SE));
dot(vert[1] / 2, L=Label('$M_2$', align=S / 5 + W));
dot((vert[0] + vert[1]) / 3, L=Label('$C_1$'), align=(vert[0] + vert[1]) / 6);
draw(o -- vert[0] -- vert[1] -- cycle);

for (int k = 0; k < 2; ++k) {
  pair m = vert[k] / 2;
  pair n = norm[k];

  draw(o -- m);
  draw(m - 2n -- m + 2n);
}

draw((-lim, -lim) -- (-lim, lim) -- (lim, lim) -- (lim, -lim) -- cycle);
limits(min=(-lim, -lim), max=(lim, lim), crop=Crop);

newpage();

for (int k = 0; k < n; ++k) {
  pair m = vert[k] / 2;
  pair d = 4norm[k];
  pair m_ = -4m;

  fill(m - d -- m + d -- m_ + d -- m_ - d -- cycle, black + opacity(0.075));
}

dot(o);

for (int k = 0; k < n; ++k) {
  dot(vert[k]);
}

draw(rotate(30) * regular_polygon(6, 1 / sqrt(3)), densely_dashed + darkgray);

draw((-lim, -lim) -- (-lim, lim) -- (lim, lim) -- (lim, -lim) -- cycle);
limits(min=(-lim, -lim), max=(lim, lim), crop=Crop);
