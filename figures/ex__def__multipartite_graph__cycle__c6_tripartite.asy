unitsize(1.5cm);

from notebook access grdraw, CycleGraph;

int[] points = new int[] { 0, 7, 12, 1, 6, 13 };

CycleGraph cg = CycleGraph(18);

for (int i = 0; i < points.length; ++i) {
  grdraw.vert(cg.vert[points[i]]);
  grdraw.edge(
    cg.vert[points[i]],
    cg.vert[points[(i + 1) % points.length]]
  );
}
