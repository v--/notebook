\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/forest}
\LoadClass[tikz]{standalone}

\RequirePackage{mathtools}
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage{forest}

\RequirePackage{packages/fonts}
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/paired_delimiters}

\usetikzlibrary{shapes.geometric}

\forestset{
  SubTree/.style={
    font=\scriptsize,
    child anchor=parent,
    draw,
    isosceles triangle,
    isosceles triangle apex angle=60,
    shape border rotate=90,
    inner sep=1pt,
    outer sep=0,
    text width={#1},
    text centered,
    text depth={#1 / 5}
  },
  SubTree/.default=1.5em,
  SmallSubTree/.style={SubTree=1em}
}
