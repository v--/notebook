import graph;

struct PointLattice {
  picture subpic;
  pair u;
  pair v;
  int n;
  int lim;
  real unit_size;
  transform t;

  void operator init(pair u, pair v, int n = 6, real unit_size = 0.5cm, transform t = identity) {
    this.u = u;
    this.v = v;
    this.n = n;
    this.unit_size = unit_size;
    this.t = t;
    unitsize(this.subpic, this.unit_size);

    transform basis_t = (0, 0, this.u.x, this.v.x, this.u.y, this.v.y);
    transform inv = inverse(t * basis_t);
    this.lim = ceil(this.n / 2 * max(abs(inv * (1, 1)), abs(inv * (-1, 1)))) + 1;
  }

  void rescale(real unit_size) {
    this.unit_size = unit_size;
    unitsize(this.subpic, this.unit_size);
  }

  void clear_subpic() {
    picture new_subpic;
    unitsize(new_subpic, this.unit_size);
    this.subpic = new_subpic;
  }

  void draw_on_subpic(bool draw_dots = true, bool draw_grid = false, bool draw_basis = false, pen dot_drawpen = black, path pth = nullpath, pen pth_drawpen = mediumgray, pen pth_fillpen = lightgray) {
    if (pth != nullpath) {
      for (int a = -this.lim; a < this.lim; ++a) {
        for (int b = -this.lim; b < this.lim; ++b) {
          pair o = t * (a * this.u + b * this.v);
          filldraw(this.subpic, shift(o) * pth, fillpen=pth_fillpen, drawpen=pth_drawpen);
        }
      }
    }

    for (int a = -this.lim; a < this.lim; ++a) {
      for (int b = -this.lim; b < this.lim; ++b) {
        pair o = t * (a * this.u + b * this.v);

        if (draw_dots) {
          dot(this.subpic, o, dot_drawpen);
        }

        if (draw_grid || draw_basis) {
          pair p = t * ((a + 1) * this.u + b * this.v);
          pair q = t * (a * this.u + (b + 1) * this.v);

          if (draw_basis && a == 0 && b == 0) {
            draw(this.subpic, o -- p, linewidth(1), Arrow(size=5));
            draw(this.subpic, o -- q, linewidth(1), Arrow(size=5));
          } else if (draw_grid) {
            draw(this.subpic, o -- p, dotted);
            draw(this.subpic, o -- q, dotted);
          }
        }
      }
    }
  }

  void redraw_on_points(picture p) {
    for (int a = -this.lim; a < this.lim; ++a) {
      for (int b = -this.lim; b < this.lim; ++b) {
        pair o = t * (a * this.u + b * this.v);
        add(this.subpic, p, o);
      }
    }
  }

  void clip_subpic(bool draw_frame = true) {
    pair ur = (this.n + 1) / 2 * (1, 1); // Upper right

    if (draw_frame) {
      draw(this.subpic, ur -- (ur.x, -ur.y) -- -ur -- (-ur.x, ur.y) -- cycle);
    }

    limits(this.subpic, min=-ur, max=ur, crop=Crop);
  }

  void draw_subpic(picture p = currentpicture) {
    add(p, this.subpic, (0, 0));
  }

  void draw(bool draw_dots = true, bool draw_grid = false, bool draw_basis = false, bool draw_frame = true, pen dot_drawpen = black, path pth = nullpath, pen pth_drawpen = mediumgray, pen pth_fillpen = lightgray, picture p = currentpicture) {
    this.clear_subpic();
    this.draw_on_subpic(draw_dots, draw_grid, draw_basis, dot_drawpen, pth, pth_drawpen, pth_fillpen);
    this.clip_subpic(draw_frame);
    this.draw_subpic(p=p);
  }
}
