\ExplSyntaxOn

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/notebook}

\LoadClass
  [
    bibliography=totocnumbered,
    numbers=endperiod,
    twoside=false
  ]
  {scrbook}

\RequirePackage{typearea}
\RedeclareSectionCommand[tocnumwidth=3em]{section}

% Generic math packages (load first to avoid misbehaving macros later)
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{empheq}
\RequirePackage{amsthm}
\RequirePackage{thmtools}

% Citations
\RequirePackage
  [
    block=ragged,
    backend=biber,
    style=alphabetic,
    citestyle=alphabetic,
    datamodel=classes/bibmodel
  ]
  {biblatex}

% Internationalization
\RequirePackage[english]{babel}
\RequirePackage[autostyle]{csquotes}

% Misc nonmath packages
\RequirePackage{subcaption}
\RequirePackage{booktabs}
\RequirePackage{seqsplit}
\RequirePackage{xspace}
\RequirePackage{enumitem}
\RequirePackage{graphbox} % \includegraphics[align=?]
\RequirePackage{csquotes}
\RequirePackage{numprint}
\RequirePackage{blkarray}
\RequirePackage{diagbox}
\RequirePackage{paracol}
\RequirePackage{forest}

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

\RequirePackage[x11names]{xcolor}
\hypersetup
  {
    linkcolor=DeepSkyBlue3,
    citecolor=DeepSkyBlue3,
    urlcolor=DeepSkyBlue3,
    filecolor=Coral4,
    menucolor=Coral4,
    runcolor=Coral4,
    linkbordercolor=DeepSkyBlue3,
    citebordercolor=DeepSkyBlue3,
    urlbordercolor=DeepSkyBlue3,
    filebordercolor=Coral4,
    menubordercolor=Coral4,
    runbordercolor=Coral4
  }

\RequirePackage[nameinlink]{cleveref}
\RequirePackage{crossreftools}

% Misc math packages
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage{diffcoeff}
\RequirePackage{ebproof}
\RequirePackage{bigints}
\RequirePackage{cancel}

% Custom code
\RequirePackage{packages/fonts}
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/paired_delimiters}
\RequirePackage{packages/bibliography}
\RequirePackage{packages/references}
\RequirePackage{packages/subproofs}
\RequirePackage{packages/theorems}
\RequirePackage{packages/metadata}

% All paracol margins will go to the right and then \reversemarginpar will put them on the left
\marginparthreshold{0}

% % Use the left margins rather than the right margins
\reversemarginpar

\ExplSyntaxOff
