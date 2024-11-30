import geometry;

import 'asymptote/labels.asy' as labels;

void draw_segment(segment seg, string LA = '', string LB = '') {
  draw(seg);

  if (LA == '') {
    dot(seg.A);
  } else {
    dot(seg.A, L=Label(LA, align=-align_oppose(seg)));
  }

  if (LB == '') {
    dot(seg.B);
  } else {
    dot(seg.B, L=Label(LB, align=align_oppose(seg)));
  }

}
