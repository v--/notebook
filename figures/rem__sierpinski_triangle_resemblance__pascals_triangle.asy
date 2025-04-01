unitsize(0.3cm);

int n = 32;
int[][] values = new int[n][n];

pair o = (0, 0);
pair u = unit((1, -sqrt(3)));
pair v = unit((1, sqrt(3)));

for (int i = 0; i < n; ++i) {
  for (int j = 0; i + j < n; ++j) {
    if (i == 0 || j == 0) {
      values[i][j] = 1;
    } else {
      values[i][j] = values[i - 1][j] + values[i][j - 1];
    }

    pair p = i * u - j * v;

    if (values[i][j] % 2 == 1) {
      fill(shift(i * u - j * v) * scale(1 / 2) * unitcircle);
    }
  }
}
