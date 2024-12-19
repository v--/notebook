unitsize(1cm);

int n = 7;
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

    label(string(values[i][j]), i * u - j * v);
  }
}
