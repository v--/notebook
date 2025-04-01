from 'asymptote/square_grid_automaton/grid.asy' access CellularAutomatonGrid;
from 'asymptote/square_grid_automaton/bounds.asy' access GridBounds, bound_union, bounds_from_cells, expand_bounds;
from 'asymptote/square_grid_automaton/neighborhood.asy' access SquareGridNeighborhood, get_moore_neighborhood;

typedef bool LocalCellularAutomatonGridEvolution(CellularAutomatonGrid grid, pair cell, SquareGridNeighborhood neighborhood);

struct SquareGridAutomatonHistory {
  CellularAutomatonGrid[] grids;
  GridBounds bounds;

  void add_grid(CellularAutomatonGrid grid) {
    this.grids.push(grid);
    this.bounds = bound_union(this.bounds, grid.get_bounds());
  }

  void draw_all() {
    for (int i = 0; i < this.grids.length; ++i) {
      this.grids[i].draw(this.bounds);
      newpage();
    }
  }
}

struct SquareGridAutomaton {
  CellularAutomatonGrid grid;
  SquareGridNeighborhood neighborhood;
  LocalCellularAutomatonGridEvolution local_evolution;

  void operator init(
    pair[] marked,
    LocalCellularAutomatonGridEvolution local_evolution,
    SquareGridNeighborhood neighborhood = get_moore_neighborhood(1),
    real unit_size = 0.4cm
  ) {
    this.grid = CellularAutomatonGrid(unit_size, marked);
    this.local_evolution = local_evolution;
    this.neighborhood = neighborhood;
  }

  SquareGridAutomatonHistory simulate(int iterations = 1) {
    SquareGridAutomatonHistory history;

    CellularAutomatonGrid active_grid = this.grid;
    CellularAutomatonGrid buffer_grid = active_grid.clone();

    for (int it = 0; it < iterations; ++it) {
      history.add_grid(active_grid);

      for (int i = 0; i < active_grid.marked.length; ++i) {
        pair cell = active_grid.marked[i];

        buffer_grid.set_state(
          cell,
          this.local_evolution(active_grid, cell, this.neighborhood.shift(cell))
        );

        for (int j = 0; j < this.neighborhood.cells.length; ++j) {
          pair shifted_cell = cell + this.neighborhood.cells[j];

          buffer_grid.set_state(
            shifted_cell,
            this.local_evolution(active_grid, shifted_cell, this.neighborhood.shift(shifted_cell))
          );
        }
      }

      active_grid = buffer_grid;
      buffer_grid = active_grid.clone();
    }

    history.add_grid(active_grid);
    history.bounds = expand_bounds(history.bounds, this.neighborhood);
    return history;
  }
}
