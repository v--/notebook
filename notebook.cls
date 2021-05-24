\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass[
  headings=standardclasses,
  bibliography=totocnumbered
]{scrartcl}

\ExplSyntaxOn

% Fonts
% I avoid fontspec and unicode-math (and hence XeTeX/LuaTeX) because they drastically slow down the compilation
\RequirePackage{stix2} % Math and T1/OT2 serif fonts
\RequirePackage{libertineRoman} % T2A serif fonts that are close to STIX Two
\RequirePackage{biolinum} % Sans-serif fonts

% Generic math packages
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{amsthm}
\RequirePackage{xfrac}
\RequirePackage{thmtools}

% Reference packages
\RequirePackage[colorlinks,unicode]{hyperref}
%% https://tex.stackexchange.com/a/525297
\RequirePackage{xcolor}

\NewDocumentCommand \setcolor {mmm}
{
  \definecolor{Hy#1color}{#2}{#3}
  \hypersetup{#1color=Hy#1color}
}

\setcolor{link}{HTML}{800006}
\setcolor{cite}{HTML}{2E7E2A}
\setcolor{file}{HTML}{131877}
\setcolor{url} {HTML}{8A0087}
\setcolor{menu}{HTML}{727500}
\setcolor{run} {HTML}{137776}

\RequirePackage{cleveref}

% Internationalization
%% I don't really need internationalization but this switches between T1 and T2A fonts where appropriate.
%% I could also perform the switch manually but the babel code was already in place.
\RequirePackage[base]{babel}

%% Relax some conflicting macros in the Russian and Bulgarian babel files
\AfterBabelLanguage{bulgarian}
{
  \let\sh\relax
  \let\ch\relax
  \let\tg\relax
  \let\ctg\relax
  \let\arctg\relax
  \let\arcctg\relax
  \let\cth\relax
  \let\cosec\relax
}

\AfterBabelLanguage{russian}
{
  \let\Prob\relax
}

%% This definition came up after a lot of attempts to make the Russian and Bulgarian babel files work together
\def\bulgarianhyphenmins{\tw@ \tw@}

\RequirePackage[main=english,russian,bulgarian]{babel}
\RequirePackage[autostyle]{csquotes}

% Citations
\RequirePackage[
  backend=biber,
  style=alphabetic,
  citestyle=alphabetic
]{biblatex}

\AtBeginBibliography
{
  \fontencoding{T2A}
  \selectfont
}

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
