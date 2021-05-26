\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{notebook}

\LoadClass
  [
    numbers=endperiod,
    bibliography=totocnumbered
  ]
  {scrartcl}

\ExplSyntaxOn

\keys_define:nn {git_commit_info}
  {
    hash .tl_set:N = \l_git_commit_info_hash_tl,
    date .tl_set:N = \l_git_commit_info_date_tl
  }

\ior_new:N \l_git_commit_info_file_stream

\NewDocumentCommand \GitCommitInfoRead {mm}
  {
    \IfFileExists { #1 }
    {
      \ior_open:Nn \l_git_commit_info_file_stream { #1 }
      \ior_get:NN  \l_git_commit_info_file_stream \l_tmpa_tl
      \ior_close:N \l_git_commit_info_file_stream

      \keys_set:nV {git_commit_info} \l_tmpa_tl
    }
    {
      \tl_set:Nn \l_git_commit_info_hash_tl {unspecified}
      \tl_set:Nn \l_git_commit_info_date_tl {\today}
    }

    \NewDocumentCommand \GitCommitInfoHash {} { \tl_use:N \l_git_commit_info_hash_tl }
    \NewDocumentCommand \GitCommitInfoDate {} { \tl_use:N \l_git_commit_info_date_tl }

    #2
  }

% Generic math packages
\RequirePackage{mathtools} % Loads amsmath
\RequirePackage{amsthm}
\RequirePackage{thmtools}

% Fonts
%% I avoid fontspec and unicode-math (and hence XeTeX/LuaTeX) because they drastically slow down the compilation
\RequirePackage[T2A,T1]{fontenc}
\RequirePackage[not1]{stix2}
\RequirePackage[sans,tt=false,ScaleRM=1.075]{libertinus} % Sans-serif
\DeclareFontFamilySubstitution{T2A}{stix2}{LibertinusSerif-TLF} % Fallback font that looks similar to STIX Two Text
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
\RequirePackage{enumitem}
\RequirePackage{imakeidx}
\RequirePackage{graphicx}

% Misc math packages
\RequirePackage[altpo,epsilon]{backnaur}
\RequirePackage[ISO]{diffcoeff}
\RequirePackage{ebproof}
\RequirePackage{bigints}
\RequirePackage{xfrac}

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
