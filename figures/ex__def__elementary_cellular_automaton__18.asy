from notebook access ElementaryCellularAutomaton;

ElementaryCellularAutomaton aut = ElementaryCellularAutomaton(
  rule=18,
  initial=new int[] { 0 },
  unit_size=0.2cm
);

aut.draw(iterations=31, draw_borders=false);
newpage();
