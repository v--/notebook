struct ElementaryCellularAutomaton {
  picture subpic;
  int rule;
  int[] initial;
  real unit_size;

  void operator init(int rule, int[] initial, real unit_size = 0.4cm) {
    this.unit_size = unit_size;
    this.rule = rule;
    this.initial = initial;
    unitsize(this.subpic, this.unit_size);
  }

  bool compute_state(bool left_state, bool center_state, bool right_state) {
    if (!left_state && !center_state && !right_state && AND(this.rule, 1) > 0) {
      return true;
    }

    if (!left_state && !center_state && right_state && AND(this.rule, 2) > 0) {
      return true;
    }

    if (!left_state && center_state && !right_state && AND(this.rule, 4) > 0) {
      return true;
    }

    if (!left_state && center_state && right_state && AND(this.rule, 8) > 0) {
      return true;
    }

    if (left_state && !center_state && !right_state && AND(this.rule, 16) > 0) {
      return true;
    }

    if (left_state && !center_state && right_state && AND(this.rule, 32) > 0) {
      return true;
    }

    if (left_state && center_state && !right_state && AND(this.rule, 64) > 0) {
      return true;
    }

    if (left_state && center_state && right_state && AND(this.rule, 128) > 0) {
      return true;
    }

    return false;
  }

  void draw_on_subpic(int iterations, bool draw_borders = true) {
    int min_bound = min(this.initial) - iterations - 1;
    int max_bound = max(this.initial) + iterations + 1;
    bool[] marked = array(max_bound - min_bound + 1, false);

    for (int it = 0; it <= iterations; ++it) {
      bool last_cell = false;

      if (it == 0) {
        for (int i = 0; i < this.initial.length; ++i) {
          marked[this.initial[i] - min_bound] = true;
        }
      } else {
        for (int i = 1; i < max_bound - min_bound; ++i) {
          bool new_state = this.compute_state(last_cell, marked[i], marked[i + 1]);
          last_cell = marked[i];
          marked[i] = new_state;
        }
      }

      for (int i = 1; i < max_bound - min_bound; ++i) {
        pair cell = (i, -it);
        path p = shift(cell) * unitsquare;

        if (draw_borders) {
          filldraw(this.subpic, p, drawpen=gray, fillpen=marked[i] ? black : white);
        } else if (marked[i]) {
          fill(this.subpic, p, p=black);
        }
      }
    }
  }

  void draw_subpic(picture p = currentpicture) {
    add(p, this.subpic, (0, 0));
  }

  void draw(picture p = currentpicture, int iterations, bool draw_borders = true) {
    this.draw_on_subpic(iterations=iterations, draw_borders=draw_borders);
    this.draw_subpic(p=p);
  }
}
