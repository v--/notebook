\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/tikzcd}
\LoadClass[tikz]{standalone}

\RequirePackage{stix2}
\RequirePackage{mathtools}

\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/unicode_math_symbols}
\RequirePackage{packages/paired_delimiters}

\usetikzlibrary{cd,shapes.geometric,fit,automata}
\tikzcdset{arrow style=math font}
\tikzset
  {
    NatTrans/.style=
      {
        commutative diagrams/.cd,
        shorten <= 2pt,
        shorten >= 2pt,
        Rightarrow
      },
    HeavyDraw/.style=
      {
        draw,
        line width=0.25mm
      },
    HeavyFill/.style=
      {
        fill,
        fill opacity=0.4
      },
    LightDraw/.style=
      {
        dashed,
        draw,
        draw opacity=0.5
      },
    LightFill/.style=
      {
        fill,
        fill opacity=0.2
      },
    % https://tikz.dev/library-automata
    initial text=
  }
