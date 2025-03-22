unitsize(1.5cm);

from notebook access grdraw, ExampleFlowGraph;

pair[] vertices;

vertices[1] =  ( 0,  0);
vertices[2] =  ( 0,  1);
vertices[3] =  ( 0, -1);
vertices[4] =  (-1,  1);
vertices[5] =  (-1, -1);
vertices[6] =  ( 1, -1);
vertices[7] =  ( 1,  1);
vertices[8] =  (-1,  0);
vertices[9] =  ( 1,  0);
vertices[10] = ( 0, -2);
vertices[11] = ( 0,  2);
vertices[13] = (-3, -2);
vertices[14] = ( 2,  1);
vertices[16] = (-2, -1);
vertices[17] = (-2,  1);
vertices[20] = (-1, -2);
vertices[22] = ( 1,  2);
vertices[26] = (-3, -1);
vertices[28] = ( 2,  0);
vertices[34] = (-1,  2);
vertices[40] = (-2, -2);
vertices[52] = (-2,  0);

int collatz(int n) {
  return (n % 2 == 0) ? n # 2 : 3 * n + 1;
}

for (int i = 1; i < vertices.length; ++i) {
  if (!vertices.initialized(i))
    continue;

  label(string(i), vertices[i]);

  int j = collatz(i);

  if (vertices.initialized(j)) {
    grdraw.edge(vertices[i], vertices[j], vertex_offset=0.2, is_arc=true);
  }
}
