from notebook access ElementaryCellularAutomaton;

for (int i = 1; i <= 3; ++i) {
  ElementaryCellularAutomaton aut = ElementaryCellularAutomaton(
    rule=i,
    initial=new int[] { 0 }
  );

  aut.draw(iterations=10);
  newpage();
}
