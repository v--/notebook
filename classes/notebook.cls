\ExplSyntaxOn

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
\RequirePackage
  [
    colorlinks,
    unicode,
    hypertexnames=false,
    hyperfootnotes=false %% The footnote hyperlinks are disabled because they are incompatible with paracol
  ]
  {hyperref}

%% Based on https://tex.stackexchange.com/a/525297
\RequirePackage{xcolor}

\cs_new_protected:Nn \nb_set_hyperref_color:nn
  {
    \definecolor{Hy#1color}{HTML}{#2}
    \hypersetup{#1color=Hy#1color}
  }

\nb_set_hyperref_color:nn {link} {800006}
\nb_set_hyperref_color:nn {cite} {2E7E2A}
\nb_set_hyperref_color:nn {file} {131877}
\nb_set_hyperref_color:nn {url}  {8A0087}
\nb_set_hyperref_color:nn {menu} {727500}
\nb_set_hyperref_color:nn {run}  {137776}

\RequirePackage[nameinlink]{cleveref}
\RequirePackage{crossreftools}

% Misc math packages
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage{diffcoeff}
\RequirePackage{blkarray}
\RequirePackage{ebproof}
\RequirePackage{bigints}
\RequirePackage{diagbox}
\RequirePackage{abraces}
\RequirePackage{forest}
\RequirePackage{cancel}

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

\ExplSyntaxOff
