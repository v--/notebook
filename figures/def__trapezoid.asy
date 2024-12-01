unitsize(1cm);

pair A = (0, 0);
pair B = (4, 0);
pair C = (3, 2);
pair D = (2, 2);

dot(A, L=Label('$A$', align=SW));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=NE));
dot(D, L=Label('$D$', align=NW));

draw(A -- B);
draw(A -- C, dashed);
draw(B -- C);
draw(B -- D, dashed);
draw(C -- D);
draw(D -- A);
