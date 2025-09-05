unitsize(1.5cm);

from notebook access grdraw, CubeGraph;

CubeGraph cg = CubeGraph(segments=1, dist=4, y_factor=2 / 3);
cg.draw_vertices();
cg.draw_edge(oriented=true);

label(cg.vertices[0][0][0], "$\mathrm{\lambda}_\rightarrow$", align=2SW);
label(cg.vertices[1][0][0], "$\mathrm{\lambda} P$", align=2S);

label(cg.vertices[0][1][0], "$\mathrm{\lambda} 2$", align=2W);
label(cg.vertices[1][1][0], "$\mathrm{\lambda} P 2$", align=2SE);

label(cg.vertices[0][0][1], "$\mathrm{\lambda} \underline{\omega}$", align=2NW);
label(cg.vertices[1][0][1], "$\mathrm{\lambda} P \underline{\omega}$", align=2SE);

label(cg.vertices[0][1][1], "$\mathrm{\lambda} \omega$", align=2NW);
label(cg.vertices[1][1][1], "$\mathrm{\lambda} P \omega$", align=2NE);

grdraw.edge(cg.vertices[0][0][0], cg.vertices[1][0][0], bold=true, is_arc=true);
label((cg.vertices[0][0][0] + cg.vertices[1][0][0]) / 2, "$(\ast, \Box)$", align=S);

grdraw.edge(cg.vertices[0][0][0], cg.vertices[0][1][0], bold=true, is_arc=true);
label((cg.vertices[0][0][0] + cg.vertices[0][1][0]) / 2, "$(\Box, \ast)$", align=W);

grdraw.edge(cg.vertices[0][0][0], cg.vertices[0][0][1], bold=true, is_arc=true);
label((cg.vertices[0][0][0] + cg.vertices[0][0][1]) / 2, "$(\Box, \Box)$", align=3E);
