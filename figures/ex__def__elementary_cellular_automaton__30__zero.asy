from notebook access ElementaryCellularAutomaton;

ElementaryCellularAutomaton aut = ElementaryCellularAutomaton(
  rule=30,
  initial=new int[] { 0 }
);

aut.draw(iterations=15);
