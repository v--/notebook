unitsize(1cm);

pair A = (0, 0);
pair B = (4, 0);
pair C = (5, 2);
pair D = (1, 2);

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=NE));
dot(D, L=Label('$D$', align=NW));

draw(A -- B);
draw(B -- C);
draw(C -- D);
draw(D -- A);
