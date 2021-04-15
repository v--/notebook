function footnote_translations(translations)
  if translations == nil then
    return
  end

  footnote = ''

  for token in string.gmatch(translations, '([^,]+)%s*') do
    key, value = string.match(token, '(%w+)=(.*)')
    translated_value = value

    if key == 'bg' then
      translated_value = '\\foreignlanguage{bulgarian}{' .. value .. '}'
    elseif key == 'ru' then
      translated_value = '\\foreignlanguage{russian}{' .. value .. '}'
    end

    if footnote == '' then
      footnote = key .. ': ' .. translated_value
    else
      footnote = footnote .. '; ' .. key .. ': ' .. translated_value
    end
  end

  if footnote ~= '' then
    tex.print('\\footnote{' .. footnote .. '}')
  end
end
