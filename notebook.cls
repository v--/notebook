\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass
  [
    numbers=endperiod,
    bibliography=totocnumbered
  ]
  {scrartcl}

\RedeclareSectionCommand[tocnumwidth=2.2em]{section}
\RedeclareSectionCommand[tocnumwidth=2.9em]{subsection}

% Generic math packages (load first to avoid misbehaving macros later)
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{empheq}
\RequirePackage{amsthm}
\RequirePackage{thmtools}

% Fonts
%% I avoid fontspec and unicode-math (and hence XeTeX/LuaTeX) because they drastically slow down the compilation
\RequirePackage[T2A,T1]{fontenc}
\RequirePackage[not1]{stix2} % Serf and math font families; load after amsmath despite documentation, it breaks otherwise
\RequirePackage[sans,tt=false,ScaleRM=1.075]{libertinus} % Sans-serif
\DeclareFontFamilySubstitution{T2A}{stix2}{LibertinusSerif-TLF} % Fallback font that looks similar to STIX Two Text
\UseLegacyTextSymbols % https://github.com/latex3/latex2e/issues/502
\RequirePackage{microtype}

% Reference packages
\RequirePackage[colorlinks,unicode]{hyperref}
%% https://tex.stackexchange.com/a/525297
\RequirePackage{xcolor}

\NewDocumentCommand \boldtt {m}
  {
    \DeclareFontFamilySubstitution{T1}{cmtt}{lmtt} % Use the slightly heavier latin modern typewriter font
    #1
  }

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
\selectfont
\RequirePackage
  [
    backend=biber,
    style=alphabetic,
    citestyle=alphabetic
  ]
  {biblatex}

\AtBeginBibliography
  {
    \fontencoding{T2A}
    \selectfont
  }

% Misc nonmath packages
\RequirePackage{xspace}
\RequirePackage{enumitem}
\RequirePackage{imakeidx}
\RequirePackage{graphicx}
\RequirePackage{crossreftools}

% Misc math packages
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage[ISO]{diffcoeff}
\RequirePackage{synttree}
\RequirePackage{ebproof}
\RequirePackage{bigints}
\RequirePackage{xfrac}

% Custom code
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/unicode_math_symbols}
\RequirePackage{packages/paired_delimiters}
\RequirePackage{packages/references}
\RequirePackage{packages/subproofs}
\RequirePackage{packages/theorems}
\RequirePackage{packages/git_commit_info}

% Use the left margins rather than the right margins
\reversemarginpar
