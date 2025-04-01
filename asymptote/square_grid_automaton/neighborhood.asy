struct SquareGridNeighborhood {
  pair[] cells;

  void operator init(pair[] cells) {
    this.cells = cells;
  }

  SquareGridNeighborhood shift(pair offset) {
    pair[] new_cells;

    for (int i = 0; i < this.cells.length; ++i) {
      new_cells.push(this.cells[i] + offset);
    }

    return SquareGridNeighborhood(new_cells);
  }
}

SquareGridNeighborhood get_moore_neighborhood(int radius = 1) {
  pair[] cells;

  for (int x = -radius; x <= radius; ++x) {
    for (int y = -radius; y <= radius; ++y) {
      cells.push((x, y));
    }
  }

  return SquareGridNeighborhood(cells);
}
