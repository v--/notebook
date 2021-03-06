function footnote_translations(translations)
  if translations == nil then
    return
  end

  footnote = ''

  for token in string.gmatch(translations, '([^,]+)%s*') do
    key, value = string.match(token, '(%w+)=(.*)')

    if footnote == '' then
      footnote = key .. ': ' .. value
    else
      footnote = footnote .. '; ' .. key .. ': ' .. value
    end
  end

  if footnote ~= '' then
    tex.print('\\footnote{' .. footnote .. '}')
  end
end
