% Assume we have the following
% playfield: the playfield, grayscale image
% vPosSynth: column indexes of playfield boundaries
% hPosSynth: row indexes of playfield boundaries
% field types, 0=bg, 1=input, 2= symbol or operator

% Load symbol library
symbolNames = "0123456789+-/x=-=";
symbolLib = cell(14,1);
for sId = 0:9
  symbolLib{sId+1} = imread(sprintf('symbols/%d.png', sId)) > 128;
endfor
symbolLib{11} = imread(sprintf('operators/%s.png', 'plus')) > 128;
symbolLib{12} = imread(sprintf('operators/%s.png', 'minus')) > 128;
symbolLib{13} = imread(sprintf('operators/%s.png', 'div')) > 128;
symbolLib{14} = imread(sprintf('operators/%s.png', 'mult')) > 128;
symbolLib{15} = imread(sprintf('operators/%s.png', 'equals')) > 128;
symbolLib{16} = imread(sprintf('operators/%s.png', 'new_minus')) > 128;
symbolLib{17} = imread(sprintf('operators/%s.png', 'new_equals')) > 128;


imgS = playfield;
symbolsAtPositions = "";

mgn = 4; % margin to test for value
for idR = 1:size(fieldTypes,1)
  for idC = 1:size(fieldTypes,2)
    imgBounds = [
      hPosSynth(idR)+mgn,
      hPosSynth(idR+1)-mgn,
      vPosSynth(idC),
      vPosSynth(idC+1)];

    % match with symbols inside region
    if (fieldTypes(idR, idC) == 2)
      img = imgS(imgBounds(1):imgBounds(2), imgBounds(3):imgBounds(4));
      img = img(:,img(1,:)==mode(img(1,:)));

      symbolLibIdx = sub_find_symbols(img, symbolLib);
      x = sprintf( "%d,%d:%s", idR, idC, symbolNames( symbolLibIdx ) );
      symbolsAtPositions = [symbolsAtPositions;x];

    endif
  endfor
endfor

