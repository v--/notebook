from 'asymptote/square_grid_automaton/grid.asy' access CellularAutomatonGrid;
from 'asymptote/square_grid_automaton/neighborhood.asy' access SquareGridNeighborhood;

bool game_of_life_local_evolution(CellularAutomatonGrid grid, pair cell, SquareGridNeighborhood neighborhood) {
  int life_neighbors = 0;

  for (int k = 0; k < neighborhood.cells.length; ++k) {
    if (neighborhood.cells[k] != cell && grid.is_alive(neighborhood.cells[k])) {
      life_neighbors += 1;
    }
  }

  if (life_neighbors == 3) {
    return true;
  }

  if (life_neighbors == 2) {
    return grid.is_alive(cell);
  }

  return false;
}
