\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/forest}
\LoadClass[tikz]{standalone}

\RequirePackage{mathtools}
\RequirePackage{forest}

\RequirePackage{packages/fonts}
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/paired_delimiters}

\usetikzlibrary{shapes.geometric}

% Based on https://tex.stackexchange.com/a/208792
\forestset{
  SubTree/.style={
    isosceles triangle,
    draw,
    shape border rotate=90,
    minimum size=3.5em,
    font=\scriptsize,
    child anchor=north,
    anchor=north
  }
}
