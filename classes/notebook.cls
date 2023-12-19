\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/notebook}

\LoadClass
  [
    numbers=endperiod,
    bibliography=totocnumbered
  ]
  {scrartcl}

% Generic math packages (load first to avoid misbehaving macros later)
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{empheq}
\RequirePackage{amsthm}
\RequirePackage{thmtools}

\RedeclareSectionCommand[tocnumwidth=2.2em]{section}
\RedeclareSectionCommand[tocnumwidth=2.9em]{subsection}
\addtokomafont{section}{\clearpage}
\addtokomafont{subsection}{\clearpage}

% Citations
\RequirePackage
  [
    backend=biber,
    style=alphabetic,
    citestyle=alphabetic
  ]
  {biblatex}

% Internationalization
\RequirePackage[english]{babel}
\RequirePackage[autostyle]{csquotes}

% Misc nonmath packages
\RequirePackage{xspace}
\RequirePackage{enumitem}
\RequirePackage{graphicx}
\RequirePackage{graphbox}
\RequirePackage{csquotes}
\RequirePackage{paracol}

% Don't use separate footnotes in paracol environments
\footnotelayout{m}

% Reference packages
% Using hypertexnames=false is suggested in https://tex.stackexchange.com/a/282313 and explained in https://tex.stackexchange.com/a/3197
% Without it the log gets cluttered with insubstantial warnings
\RequirePackage[colorlinks,unicode,hypertexnames=false]{hyperref}
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

\RequirePackage[nameinlink]{cleveref}
\RequirePackage{crossreftools}

% Misc math packages
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage{diffcoeff}
\RequirePackage{blkarray}
\RequirePackage{ebproof}
\RequirePackage{bigints}
\RequirePackage{forest}
\RequirePackage{cancel}
\RequirePackage{diagbox}

% Custom code
\RequirePackage{packages/fonts}
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/paired_delimiters}
\RequirePackage{packages/references}
\RequirePackage{packages/subproofs}
\RequirePackage{packages/theorems}
\RequirePackage{packages/git_commit_info}

% Use the left margins rather than the right margins
\reversemarginpar
