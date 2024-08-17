usepackage('stix2');
unitsize(3.5cm);

pair A = (1, sqrt(3));
pair B = (0, 0);
pair C = (2, 0);

int n = 7;
int[][] values = new int[n][n];

for (int k = 0; k < n; ++k) {
  draw(B + k / n * (A - B) -- C + k / n * (A - C), mediumgray);
  draw(A + k / n * (B - A) -- C + k / n * (B - C), mediumgray);
  draw(A + k / n * (C - A) -- B + k / n * (C - B), mediumgray);
}

for (int i = 0; i < n; ++i) {
  for (int j = 0; i + j < n; ++j) {
    pair translation = i / n * (B - A) + j / n * (C - A);
    pair A_ = A + translation;
    pair B_ = B + (n - 1) / n * (A - B) + translation;
    pair C_ = C + (n - 1) / n * (A - C) + translation;
    pair pos = (A_ + B_ + C_) / 3;

    if (i == 0 || j == 0) {
      values[i][j] = 1;
    } else {
      values[i][j] = values[i - 1][j] + values[i][j - 1];
    }

    label(string(values[i][j]), pos);
  }
}
