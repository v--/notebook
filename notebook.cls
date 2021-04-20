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
% https://tex.stackexchange.com/a/525984
\RequirePackage[dvipsnames]{xcolor}

\hypersetup{
  linkcolor=NavyBlue,
  citecolor=NavyBlue,
  filecolor=Red,
  urlcolor=NavyBlue,
  menucolor=Red,
  runcolor=Red,
  linkbordercolor=NavyBlue,
  citebordercolor=NavyBlue,
  filebordercolor=Red,
  urlbordercolor=NavyBlue,
  menubordercolor=Red,
  runbordercolor=Red
}

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
