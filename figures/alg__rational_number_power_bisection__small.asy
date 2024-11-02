usepackage('stix2');
unitsize(6cm);

import 'asymptote/pens.asy' as pens;

real offset = 0.1;

int a = 50;
int b = 100;
int c = 65;
int d = 100;
int n = 3;

void draw_diagram(real l, real u, int step) {
  real m = (l + u) / 2;

  draw((0, 0) -- (1, 0));
  dot((0, 0), L=Label('$0$', align=W));
  dot((1, 0), L=Label('$1$', align=E));

  dot((a / b, 0), L=Label('$a/b$', align=abs(a/b - l) < 0.1 ? S : N));
  dot((c / d, 0), L=Label('$c/d$', align=abs(a/b - l) < 0.1 ? S : N));

  draw((l, offset) -- (u, offset));
  draw((l, 0) -- (l, offset), densely_dashed);
  draw((u, offset) -- (u, 0), densely_dashed);

  draw((l ** n, -offset) -- (u ** n, -offset));
  draw((l ** n, 0) -- (l ** n, -offset), densely_dashed);
  draw((u ** n, -offset) -- (u ** n, 0), densely_dashed);

  draw((m ** n, -offset) -- (m ** n, 0), densely_dashed);

  dot((l ** n, -offset), L=Label('$l_' + string(step) + '^n$', align=S));
  dot((m ** n, -offset), L=Label('$m_' + string(step) + '^n$', align=S));
  dot((u ** n, -offset), L=Label('$u_' + string(step) + '^n$', align=S));
  dot((l, offset), L=Label('$l_' + string(step) + '$', align=(u - l) < 0.2 ? NW : N));
  dot((m, offset), L=Label('$m_' + string(step) + '$', align=N));
  dot((u, offset), L=Label('$u_' + string(step) + '$', align=(u - l) < 0.2 ? NE : N));
}

real l0 = a / b;
real u0 = 1;
real m0 = (l0 + u0) / 2;
draw_diagram(l=l0, u=u0, step=0);

newpage();

real l1 = m0;
real u1 = u0;
real m1 = (l1 + u1) / 2;
draw_diagram(l=l1, u=u1, step=1);

newpage();

real l2 = l1;
real u2 = m1;
real m2 = (l2 + u2) / 2;
draw_diagram(l=l2, u=u2, step=2);
