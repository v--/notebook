import markers;

frame arrow_frame;
draw(arrow_frame, (0, 0) -- (2, 0), Arrow(TeXHead));

marker arrow_marker(int n) {
  return marker(markinterval(n, arrow_frame, rotated=true));
}
