function citation_target(target)
  if tonumber(target, 10) ~= nil then
    tex.print("\\\\{}page " .. target)
  elseif target ~= nil then
    tex.print("\\\\" .. target)
  end
end
