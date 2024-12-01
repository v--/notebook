unitsize(1cm);

pair O = (0, 0);
pair u = (2, 1);
pair v = (-1 / 3, -3 / 2);

dot(O, L=Label('$O$', align=S));
dot(u, L=Label('$\\tau_u(O)$', align=NE));
dot(v, L=Label('$\\tau_v(O)$', align=SW));
dot((u + v), L=Label('$\\tau_{u + v}(O)$', align=SE));
