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
  arc/.default=0.6pt
}

\NewDocumentCommand \ExampleFlowGraph {}
  {
    \node[dot, label=left: \( a \)] (a) at (0, 0)  {};
    \node[dot, label=above:\( b \)] (b) at (1, 1)  {};
    \node[dot, label=below:\( c \)] (c) at (1, -1) {};
    \node[dot, label=above:\( d \)] (d) at (3, 1)  {};
    \node[dot, label=below:\( e \)] (e) at (3, -1) {};
    \node[dot, label=below:\( f \)] (f) at (4, 0)  {};
  }

\NewDocumentCommand \GeneralizedPetersen {O{0}mm}
  {
    \pgfmathsetmacro \correction {#1};
    \pgfmathsetmacro \n {#2};
    \pgfmathsetmacro \limit {\n - 1};
    \pgfmathsetmacro \k {#3};

    \foreach \i in { 0, ..., \limit } {
      \pgfmathtruncatemacro \angle {(\i + \correction) * 360/\n};
      \node[dot] (\i_inner) at (\angle: 1) {};
      \node[dot] (\i_outer) at (\angle: 2) {};
    }

    \foreach \i in { 0, ..., \limit } {
      \pgfmathtruncatemacro \j {Mod(\i + 1, \n)};
      \draw[edge] (\i_inner) edge (\i_outer);
      \draw[edge] (\i_outer) edge (\j_outer);
    }

    \foreach \i in { 0, ..., \limit } {
      \pgfmathtruncatemacro \j {Mod(\i + \k, \n)};
      \draw[edge] (\i_inner) edge (\j_inner);
    }
  }
