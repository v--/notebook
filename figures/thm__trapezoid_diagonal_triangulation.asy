unitsize(1cm);

pair A = (0, 0);
pair B = (4, 0);
pair C = (3, 2);
pair D = (2, 2);

dot(A, L=Label('$A$', align=S));
dot(B, L=Label('$B$', align=SE));
dot(C, L=Label('$C$', align=N));
dot(D, L=Label('$D$', align=NW));

draw(A -- B);
draw(A -- C);
draw(B -- C);
draw(C -- D);
draw(D -- A);
