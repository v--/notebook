\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass[
  headings=standardclasses,
  bibliography=totocnumbered
]{scrartcl}

% Generic math packages
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{amsthm}
\RequirePackage{lualatex-math}

% Reference packages
\RequirePackage[colorlinks]{hyperref}
% https://tex.stackexchange.com/a/525297
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
\RequirePackage[english]{babel}
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

% These are generic warnings about compatibility with mathtools and are not code-related.
\RequirePackage[warnings-off={mathtools-colon,mathtools-overbracket}]{unicode-math}
\setmathfont{Stix Two Math}

\RequirePackage{microtype}
