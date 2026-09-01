\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/tikzcd}
\LoadClass[tikz]{standalone}

\RequirePackage{mathtools}

\RequirePackage{packages/fonts}
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/paired_delimiters}

\usetikzlibrary
  {
    cd,
    shapes.geometric,
    fit,
    automata
  }

\RequirePackage{packages/stix2_arrows}

\pgfkeysdef
  {/tikz/commutative diagrams/arrow style/stix2}
  {
    \tikzcdset
    {
      /tikz/commutative diagrams/arrow style/tikz,
      tikzcd implies/.tip={stix},
    }
  }

\tikzcdset{arrow style=stix2}

\tikzset
  {
    NatTrans/.style=
      {
        commutative diagrams/.cd,
        Rightarrow,
        labels={inner sep=+1ex}
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
