import geometry;

access 'asymptote/lab.asy' as lab;

void draw_segment(segment seg, string LA = '', string LB = '') {
  draw(seg);

  if (LA == '') {
    dot(seg.A);
  } else {
    dot(seg.A, L=Label(LA, align=-lab.align_oppose(seg)));
  }

  if (LB == '') {
    dot(seg.B);
  } else {
    dot(seg.B, L=Label(LB, align=lab.align_oppose(seg)));
  }

}
