import geometry;

pair align_oppose(pair base, pair opposite) {
  return unit(base - opposite);
}

pair align_oppose(segment seg) {
  return unit(seg.B - seg.A);
}
