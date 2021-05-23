\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass[
  headings=standardclasses,
  bibliography=totocnumbered
]{scrartcl}

\ExplSyntaxOn

% Fonts
\RequirePackage[T2A]{fontenc}
\RequirePackage{microtype}

% Generic math packages
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{amsthm}
\RequirePackage{amssymb}
\RequirePackage{xfrac}
\RequirePackage{thmtools}

%% Consolation for unicode-math; See symbols.sty
\RequirePackage{mathabx} % \lsemantic \rsemantic \bigast \Dashv

% Reference packages
\RequirePackage[colorlinks, unicode]{hyperref}
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
\let\setcolor\relax

\RequirePackage{cleveref}

% Internationalization
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

\RequirePackage[main=english, russian, bulgarian, italian]{babel}
\RequirePackage[autostyle]{csquotes}

% Citations
\RequirePackage[
  backend=biber,
  autolang=other,
  style=alphabetic,
  citestyle=alphabetic
]{biblatex}

% Misc nonmath packages
\RequirePackage{enumitem}
\RequirePackage{imakeidx}
\RequirePackage{graphicx}

% Misc math packages
\RequirePackage[altpo, epsilon]{backnaur}
\RequirePackage[ISO]{diffcoeff}
\RequirePackage{ebproof}
\RequirePackage{bigints}

% Custom code
\RequirePackage{packages/math_macros}
\RequirePackage{packages/symbols}
\RequirePackage{packages/paired_delimiters}
\RequirePackage{packages/references}
\RequirePackage{packages/subproofs}
\RequirePackage{packages/theorem_styles}
\RequirePackage{packages/environments}

% Use the left margins rather than the right margins
\reversemarginpar

\ExplSyntaxOff
