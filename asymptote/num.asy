bool are_close(real a, real b) {
  return abs(b - a) < 1e-10;
}

bool is_nearly_zero(real a) {
  return are_close(a, 0);
}
