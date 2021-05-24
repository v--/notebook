\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass
[
  headings=standardclasses,
  bibliography=totocnumbered
]
{scrartcl}

\ExplSyntaxOn

% Fonts
%% I avoid fontspec and unicode-math (and hence XeTeX/LuaTeX) because they drastically slow down the compilation
\RequirePackage[T2A]{fontenc}
\RequirePackage[tt=false]{libertinus}
\RequirePackage{libertinust1math}
\RequirePackage{microtype}

% Generic math packages
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{amsthm}
\RequirePackage{amssymb}
\RequirePackage{xfrac}
\RequirePackage{thmtools}

% Reference packages
\RequirePackage[colorlinks,unicode]{hyperref}
%% https://tex.stackexchange.com/a/525297
\RequirePackage{xcolor}

\NewDocumentCommand \SetHRColor {mmm}
{
  \definecolor{Hy#1color}{#2}{#3}
  \hypersetup{#1color=Hy#1color}
}

\SetHRColor{link}{HTML}{800006}
\SetHRColor{cite}{HTML}{2E7E2A}
\SetHRColor{file}{HTML}{131877}
\SetHRColor{url} {HTML}{8A0087}
\SetHRColor{menu}{HTML}{727500}
\SetHRColor{run} {HTML}{137776}

\let\SetHRColor\relax

\RequirePackage{cleveref}

% Internationalization
\RequirePackage[english]{babel}
\RequirePackage[autostyle]{csquotes}

% Citations
\RequirePackage
[
  backend=biber,
  style=alphabetic,
  citestyle=alphabetic
]
{biblatex}

% Misc nonmath packages
\RequirePackage{enumitem}
\RequirePackage{imakeidx}
\RequirePackage{graphicx}

% Misc math packages
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage[ISO]{diffcoeff}
\RequirePackage{ebproof}
\RequirePackage{bigints}

% Custom code
\RequirePackage{packages/math_macros}
\RequirePackage{packages/symbols}
\RequirePackage{packages/paired_delimiters}
\RequirePackage{packages/references}
\RequirePackage{packages/subproofs}
\RequirePackage{packages/theorems}
\RequirePackage{packages/environments}

% Use the left margins rather than the right margins
\reversemarginpar

\ExplSyntaxOff
