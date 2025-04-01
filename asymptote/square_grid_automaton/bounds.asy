from 'asymptote/square_grid_automaton/neighborhood.asy' access SquareGridNeighborhood;

struct GridBounds {
  int min_x;
  int min_y;
  int max_x;
  int max_y;
}

GridBounds bounds_from_cells(pair[] cells) {
  GridBounds result;

  for (int i = 0; i < cells.length; ++i) {
    pair cell = cells[i];

    if (i == 0) {
      result.min_x = round(cell.x);
      result.max_x = round(cell.x);
      result.min_y = round(cell.y);
      result.max_y = round(cell.y);
    } else {
      result.min_x = min(result.min_x, round(cell.x));
      result.max_x = max(result.max_x, round(cell.x));
      result.min_y = min(result.min_y, round(cell.y));
      result.max_y = max(result.max_y, round(cell.y));
    }
  }

  return result;
}

GridBounds bound_union(GridBounds a, GridBounds b) {
  GridBounds result;
  result.min_x = min(a.min_x, b.min_x);
  result.max_x = max(a.max_x, b.max_x);
  result.min_y = min(a.min_y, b.min_y);
  result.max_y = max(a.max_y, b.max_y);
  return result;
}

GridBounds expand_bounds(GridBounds bounds, SquareGridNeighborhood neighborhood) {
  GridBounds result;
  GridBounds neighborhood_bounds = bounds_from_cells(neighborhood.cells);
  result.min_x = bounds.min_x + neighborhood_bounds.min_x;
  result.max_x = bounds.max_x + neighborhood_bounds.max_x;
  result.min_y = bounds.min_y + neighborhood_bounds.min_y;
  result.max_y = bounds.max_y + neighborhood_bounds.max_y;
  return result;
}
