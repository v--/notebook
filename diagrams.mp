def labeled_arrow@#(expr src, dest, text) =
  begingroup
    bboxmargin := 5pt;
    labeloffset := 8pt;
    save p;

    path p;
    p = (center src) -- (center dest) cutbefore (bbox src) cutafter (bbox dest);

    drawarrow p;
    label.@#(text, point 0.5 of p);
  endgroup
enddef;
