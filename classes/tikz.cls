\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{classes/tikz}
\LoadClass[tikz]{standalone}

\RequirePackage{mathtools}

\RequirePackage{packages/fonts}
\RequirePackage{packages/math_macros}
\RequirePackage{packages/math_environments}
\RequirePackage{packages/paired_delimiters}

% Taken from https://tex.stackexchange.com/a/445634
\pgfdeclarearrow{
  name = stix,
  parameters = {\ifpgfarrowharpoon h\fi},
  setup code = {
    \ifpgfarrowharpoon
      \pgfutil@tempdima=\dimexpr\pgflinewidth/68
      \pgfarrowssettipend{247\pgfutil@tempdima}
      \pgfarrowssetlineend{\pgfutil@tempdima}
      \pgfarrowssetbackend{-81\pgfutil@tempdima}
      \pgfarrowshullpoint{-81\pgfutil@tempdima}{224\pgfutil@tempdima}
      \pgfarrowshullpoint{-58\pgfutil@tempdima}{247\pgfutil@tempdima}
      \pgfarrowshullpoint{247\pgfutil@tempdima}{-34\pgfutil@tempdima}
      \pgfarrowshullpoint{0pt}{-34\pgfutil@tempdima}
    \else\ifpgfarrowreversed
      \pgfutil@tempdima=\dimexpr\pgflinewidth/68
      \pgfarrowssettipend{0pt}
      \pgfarrowssetlineend{-\pgfutil@tempdima}
      \pgfarrowssetbackend{-208\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-208\pgfutil@tempdima}{181\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-188\pgfutil@tempdima}{201\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{0pt}{34\pgfutil@tempdima}
    \else\ifdim\pgfinnerlinewidth>\z@
      \pgfutil@tempdima=\dimexpr\pgflinewidth/272
      \pgfarrowssettipend{324\pgfutil@tempdima}
      \pgfarrowssetlineend{\pgfutil@tempdima}
      \pgfarrowssetbackend{-73\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-73\pgfutil@tempdima}{285\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-51\pgfutil@tempdima}{305\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{324\pgfutil@tempdima}{5\pgfutil@tempdima}
    \else
      \pgfutil@tempdima=\dimexpr\pgflinewidth/68
      \pgfarrowssettipend{192\pgfutil@tempdima}
      \pgfarrowssetlineend{\pgfutil@tempdima}
      \pgfarrowssetbackend{-72\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-72\pgfutil@tempdima}{181\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-51\pgfutil@tempdima}{201\pgfutil@tempdima}
      \pgfarrowsupperhullpoint{-192\pgfutil@tempdima}{5\pgfutil@tempdima}
    \fi\fi\fi
  },
  drawing code = {
    \ifpgfarrowharpoon %% harpoon
      \pgftransformscale{\pgflinewidth/68}
      \pgfpathmoveto{\pgfpoint{0}{34}}
      \pgfpathcurveto{\pgfpoint{40}{34}}{\pgfpoint{44}{50}}{\pgfpoint{44}{66}}
      \pgfpathcurveto{\pgfpoint{44}{94}}{\pgfpoint{-22}{156}}{\pgfpoint{-81}{224}}
      \pgfpathlineto{\pgfpoint{-58}{247}}
      \pgfpathcurveto{\pgfpoint{44}{147}}{\pgfpoint{117}{66}}{\pgfpoint{247}{-30}}
      \pgfpathlineto{\pgfpoint{247}{-34}}
      \pgfpathlineto{\pgfpoint{0}{-34}}
      \pgfpathclose
      \pgfusepathqfill
    \else\ifpgfarrowreversed %% reversed arrowhead
      \pgftransformscale{\pgflinewidth/68}
      \pgfpathmoveto{\pgfpoint{0}{34}}
      \pgfpathcurveto{\pgfpoint{-73}{78}}{\pgfpoint{-134}{138}}{\pgfpoint{-188}{201}}
      \pgfpathlineto{\pgfpoint{-208}{181}}
      \pgfpathcurveto{\pgfpoint{-185}{147}}{\pgfpoint{-152}{118}}{\pgfpoint{-124}{83}}
      \pgfpathcurveto{\pgfpoint{-111}{65}}{\pgfpoint{-95}{33}}{\pgfpoint{-95}{0}}
      \pgfpathcurveto{\pgfpoint{-95}{-33}}{\pgfpoint{-111}{-65}}{\pgfpoint{-124}{-83}}
      \pgfpathcurveto{\pgfpoint{-152}{-118}}{\pgfpoint{-185}{-147}}{\pgfpoint{-208}{-181}}
      \pgfpathlineto{\pgfpoint{-188}{-201}}
      \pgfpathcurveto{\pgfpoint{-134}{-138}}{\pgfpoint{-73}{-78}}{\pgfpoint{0}{-34}}
      \pgfpathclose
      \pgfusepathqfill
    \else\ifdim\pgfinnerlinewidth>\z@ %% double arrow
      \pgftransformscale{\pgflinewidth/272}
      \pgfpathmoveto{\pgfpoint{0}{136}}
      \pgfpathcurveto{\pgfpoint{18}{136}}{\pgfpoint{27}{151}}{\pgfpoint{27}{159}}
      \pgfpathcurveto{\pgfpoint{27}{175}}{\pgfpoint{20}{184}}{\pgfpoint{3}{202}}
      \pgfpathcurveto{\pgfpoint{-8}{213}}{\pgfpoint{-48}{256}}{\pgfpoint{-73}{285}}
      \pgfpathlineto{\pgfpoint{-51}{305}}
      \pgfpathcurveto{\pgfpoint{69}{187}}{\pgfpoint{198}{100}}{\pgfpoint{324}{5}}
      \pgfpathlineto{\pgfpoint{324}{-5}}
      \pgfpathcurveto{\pgfpoint{198}{-100}}{\pgfpoint{69}{-187}}{\pgfpoint{-51}{-305}}
      \pgfpathlineto{\pgfpoint{-73}{-285}}
      \pgfpathcurveto{\pgfpoint{-48}{-256}}{\pgfpoint{-8}{-213}}{\pgfpoint{3}{-202}}
      \pgfpathcurveto{\pgfpoint{20}{-184}}{\pgfpoint{27}{-175}}{\pgfpoint{27}{-159}}
      \pgfpathcurveto{\pgfpoint{27}{-151}}{\pgfpoint{18}{-136}}{\pgfpoint{0}{-136}}
      \pgftransformreset
      \pgfpathlineto{\pgfpoint{0}{-.5*\pgfinnerlinewidth}}
      \pgftransformxshift{208\pgflinewidth/272}
      \pgftransformscale{\pgfinnerlinewidth/136}
      \pgfpathlineto{\pgfpoint{-61}{-68}}
      \pgfpathcurveto{\pgfpoint{-27}{-49}}{\pgfpoint{0}{-24}}{\pgfpoint{0}{0}}
      \pgfpathcurveto{\pgfpoint{0}{24}}{\pgfpoint{-27}{49}}{\pgfpoint{-61}{68}}
      \pgftransformreset
      \pgfpathlineto{\pgfpoint{0}{.5*\pgfinnerlinewidth}}
      \pgfpathclose
      \pgfusepathqfill
    \else %% normal arrowhead
      \pgftransformscale{\pgflinewidth/68}
      \pgfpathmoveto{\pgfpoint{0}{34}}
      \pgfpathcurveto{\pgfpoint{18}{34}}{\pgfpoint{26}{44}}{\pgfpoint{26}{54}}
      \pgfpathcurveto{\pgfpoint{26}{63}}{\pgfpoint{21}{74}}{\pgfpoint{12}{83}}
      \pgfpathcurveto{\pgfpoint{-19}{115}}{\pgfpoint{-48}{148}}{\pgfpoint{-72}{181}}
      \pgfpathlineto{\pgfpoint{-51}{201}}
      \pgfpathcurveto{\pgfpoint{16}{123}}{\pgfpoint{94}{47}}{\pgfpoint{192}{5}}
      \pgfpathlineto{\pgfpoint{192}{-5}}
      \pgfpathcurveto{\pgfpoint{94}{-47}}{\pgfpoint{16}{-123}}{\pgfpoint{-51}{-201}}
      \pgfpathlineto{\pgfpoint{-72}{-181}}
      \pgfpathcurveto{\pgfpoint{-48}{-148}}{\pgfpoint{-19}{-115}}{\pgfpoint{12}{-83}}
      \pgfpathcurveto{\pgfpoint{21}{-74}}{\pgfpoint{26}{-63}}{\pgfpoint{26}{-54}}
      \pgfpathcurveto{\pgfpoint{26}{-44}}{\pgfpoint{18}{-34}}{\pgfpoint{0}{-34}}
      \pgfpathclose
      \pgfusepathqfill
    \fi\fi\fi
  }
}
