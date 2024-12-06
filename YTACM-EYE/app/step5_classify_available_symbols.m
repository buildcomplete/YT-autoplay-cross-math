% Assume the following is avaliable
% variables % image
% varColIdx % column indexes
% varRowIdx % row indes
% rectSize % rectSize
% varIndexEnergy % the energy at a specific index, if zero the is no variable at the entry

wh = (rectSize / 2) - 5;
variables_with_pos = "";

rSymLib = symbolLib([1:10 18]);
rSymNames = symbolNames([1:10 18]);
for idR = 1:length(varRowIdx)
  for idC = 1:length(varColIdx)
    if (varIndexEnergy(idR, idC) > 0)
      r1 = varRowIdx(idR) - wh;
      r2 = varRowIdx(idR) + wh;
      c1 = varColIdx(idC) - wh;
      c2 = varColIdx(idC) + wh;

      I = variables(r1:r2, c1:c2);
      B = (1 - (I < I(1)-10)) .* 255; % Remove shadow noise by binarization, assuming dark letter on brighter bg

      sIds = sub_find_symbols(B, rSymLib);
      variables_with_pos = [variables_with_pos; sprintf("%d,%d:%s", idR, idC, rSymNames(sIds))];
    endif
  end
end
