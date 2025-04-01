from 'asymptote/square_grid_automaton/bounds.asy' access GridBounds, bounds_from_cells;

struct CellularAutomatonGrid {
  picture subpic;
  real unit_size;
  pair[] marked;

  void operator init(real unit_size = 0.5cm, pair[] marked = {}) {
    this.unit_size = unit_size;
    this.marked = marked;
    unitsize(this.subpic, this.unit_size);
  }

  bool is_alive(pair cell) {
    for (int i = 0; i < this.marked.length; ++i) {
      if (this.marked[i] == cell) {
        return true;
      }
    }

    return false;
  }

  void set_state(pair cell, bool state) {
    for (int i = 0; i < this.marked.length; ++i) {
      if (this.marked[i] == cell) {
        if (!state) {
          this.marked.delete(i);
        }

        return;
      }
    }

    if (state) {
      this.marked.push(cell);
    }
  }

  GridBounds get_bounds() {
    return bounds_from_cells(this.marked);
  }

  void draw_on_subpic(GridBounds bounds) {
    for (int x = bounds.min_x; x <= bounds.max_x; ++x) {
      for (int y = bounds.min_y; y <= bounds.max_y; ++y) {
        pair cell = (x, y);
        filldraw(this.subpic, shift(cell) * unitsquare, drawpen=gray, fillpen=this.is_alive(cell) ? black : white);
      }
    }
  }

  void draw_subpic(picture p = currentpicture) {
    add(p, this.subpic, (0, 0));
  }

  void draw(GridBounds bounds, picture p = currentpicture) {
    this.draw_on_subpic(bounds);
    this.draw_subpic(p=p);
  }

  CellularAutomatonGrid clone() {
    return CellularAutomatonGrid(this.unit_size, copy(this.marked));
  }
}
