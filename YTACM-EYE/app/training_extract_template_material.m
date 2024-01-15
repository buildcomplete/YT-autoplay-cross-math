% Helper to extact boxes with symbols to use for later template matching

% Assuming the following is avaliable
% setName, a string to prepend the image names when saving
% playfield: the playfield, grayscale image
% vPosSynth: column indexes of playfield boundaries
% hPosSynth: row indexes of playfield boundaries
% fieldTypes: 0=bg, 1=input, 2= symbol or operator

mgn = 4; % margin to test for value
for idR = 1:size(fieldTypes,1)
  for idC = 1:size(fieldTypes,2)
    imgBounds = [
      hPosSynth(idR)+mgn,
      hPosSynth(idR+1)-mgn,
      vPosSynth(idC)+mgn,
      vPosSynth(idC+1)-mgn];

    % Save symbols and operators
    if (fieldTypes(idR, idC) == 2)
      img = playfield(imgBounds(1):imgBounds(2), imgBounds(3):imgBounds(4));
      imwrite(img, sprintf("out/%s_%d_%d.png", setName, idR, idC));

      [symColIdx symRowIdx] = sub_find_symbol_splits(img);
      for symIdx = 1:size(symColIdx,1)
        symImg = img(symRowIdx(1):symRowIdx(2), symColIdx(symIdx,1):symColIdx(symIdx,2));
        imwrite(symImg, sprintf("out/%s_%d_%d_%d.png", setName, idR, idC, symIdx));
      endfor
    end
  endfor
endfor

