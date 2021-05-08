\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass[
  headings=standardclasses,
  bibliography=totocnumbered
]{scrartcl}

% Generic math packages
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{amsthm}
\RequirePackage{thmtools}
\RequirePackage{lualatex-math}

% Reference packages
\RequirePackage[colorlinks]{hyperref}
%% https://tex.stackexchange.com/a/525297
\RequirePackage{xcolor}

\NewDocumentCommand \setcolor {mmm} {%
  \definecolor{Hy#1color}{#2}{#3}%
  \hypersetup{#1color=Hy#1color}%
}

\setcolor{link}{HTML}{800006}
\setcolor{cite}{HTML}{2E7E2A}
\setcolor{file}{HTML}{131877}
\setcolor{url} {HTML}{8A0087}
\setcolor{menu}{HTML}{727500}
\setcolor{run} {HTML}{137776}

\RequirePackage{cleveref}

% Internationalization
\RequirePackage[base]{babel}

%% Relax some conflicting macros in the Russian and Bulgarian babel files
\ExplSyntaxOn

\AfterBabelLanguage{bulgarian}{
  \let\sh\relax
  \let\ch\relax
  \let\tg\relax
  \let\ctg\relax
  \let\arctg\relax
  \let\arcctg\relax
  \let\cth\relax
  \let\cosec\relax
}

\AfterBabelLanguage{russian}{
  \let\Prob\relax
}

\ExplSyntaxOff

%% This definition came up after a lot of attempts to make the Russian and Bulgarian babel files work together
\def\bulgarianhyphenmins{\tw@ \tw@}

\RequirePackage[main=english,russian,bulgarian]{babel}
\RequirePackage[autostyle]{csquotes}

% Citations
\RequirePackage[
  backend=biber,
  autolang=other,
  style=alphabetic,
  citestyle=alphabetic
]{biblatex}

% Fonts
\RequirePackage{fontspec}
\setmainfont{Stix Two Text}
\setsansfont{CMU Sans Serif}
\setmonofont{CMU Typewriter Text}

%% Disable generic warnings about compatibility with mathtools.
\RequirePackage[warnings-off={mathtools-colon,mathtools-overbracket}]{unicode-math}
\setmathfont{Stix Two Math}

\RequirePackage{microtype}

% Misc nonmath packages
\RequirePackage{enumitem}
\RequirePackage{imakeidx}

% Misc math packages
\RequirePackage[altpo, epsilon]{backnaur}
\RequirePackage[ISO]{diffcoeff}
\RequirePackage{ebproof}
\RequirePackage{bigints}

% Custom code
\RequirePackage{packages/math_macros}
\RequirePackage{packages/paired_delimiters}
\RequirePackage{packages/references}
\RequirePackage{packages/subproofs}
\RequirePackage{packages/theorem_styles}
\RequirePackage{packages/environments}
\RequirePackage{packages/metapost}

% Use the left margins rather than the right margins
\reversemarginpar
