\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/graphs}
\LoadClass{classes/tikz}

\tikzset{
  dot/.style={circle, draw, line width=0.6pt, minimum size=#1, inner sep=0pt, outer sep=0pt}, % Based on https://tex.stackexchange.com/a/445950
  dot/.default=4pt,
  densely dashed/.style={dash pattern=on 1pt off 1pt},
  edge/.style={line width=#1, font=\scriptsize},
  edge/.default=0.6pt,
  arc/.style={-latex, line width=#1, font=\scriptsize},
  arc/.default=0.6pt,
  example_graph_nodes/.pic={
    \node[dot, label=left: \( a \)] (a) at (0, 0)  {};
    \node[dot, label=above:\( b \)] (b) at (1, 1)  {};
    \node[dot, label=below:\( c \)] (c) at (1, -1) {};
    \node[dot, label=above:\( d \)] (d) at (3, 1)  {};
    \node[dot, label=below:\( e \)] (e) at (3, -1) {};
    \node[dot, label=below:\( f \)] (f) at (4, 0)  {};
  }
}
