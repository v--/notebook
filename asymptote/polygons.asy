import graph;

path regular_polygon(int n, real r = 1) {
  path result;

  for (int k = 0; k < n; ++k) {
    result = result -- polar(r, 2pi * k / n);
  }

  result = result -- cycle;
  return result;
}
