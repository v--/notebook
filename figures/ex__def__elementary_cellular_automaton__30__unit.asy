from notebook access ElementaryCellularAutomaton;

ElementaryCellularAutomaton aut = ElementaryCellularAutomaton(
  rule=30,
  initial=new int[] { -1, 1 }
);

aut.draw(iterations=15);
