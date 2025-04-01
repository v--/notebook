unitsize(1.5cm);

from notebook access SquareGridAutomaton, sga;

SquareGridAutomaton aut = SquareGridAutomaton(
  marked = new pair[] {
    (-1, 1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
  },
  local_evolution = sga.game_of_life_local_evolution
);

aut.simulate(4).draw_all();
