\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/tikzcd}
\LoadClass{classes/tikz}

\usetikzlibrary{cd,shapes.geometric,fit,automata}

\tikzcdset{arrow style=math font}
\tikzset{
  >=stix,
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
