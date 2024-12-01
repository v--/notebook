unitsize(1.5cm);

from notebook access grdraw, BipartiteGraph;

BipartiteGraph bg = BipartiteGraph(2, 2);
bg.draw_vertices();
bg.draw_edge_complete();

grdraw.vert(bg.left[0], L=Label('$00 \mapsto \iota_1(0)$', align=2W));
grdraw.vert(bg.left[1], L=Label('$10 \mapsto \iota_1(1)$', align=2W));

grdraw.vert(bg.right[0], L=Label('$\iota_2(0) \mapsfrom 10$', align=2E));
grdraw.vert(bg.right[1], L=Label('$\iota_2(1) \mapsfrom 11$', align=2E));
