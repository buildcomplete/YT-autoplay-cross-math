% assuming the following input

% Determine the type of what is inside the playfield grid
% playfield: the playfield, grayscale image
% vPosSynth: column indexes of playfield boundaries
% hPosSynth: row indexes of playfield boundaries


% determine type inside the grid
% fieldTypes, 0=bg, 1=input, 2= symbol or operator

X = playfield;
M = abs(X-X(1) < 3);
D1 = bwdist(M); % distance to background
D2 = bwdist(not(M)); % distance to inside boxes
stepSize = vPosSynth(2)- vPosSynth(1);

fieldTypes = zeros(length(hPosSynth)-1, length(vPosSynth)-1);

mgn = 5; % margin to test for value
for idR = 1:size(fieldTypes,1)
  for idC = 1:size(fieldTypes,2)
    center = round([
      (hPosSynth(idR) + hPosSynth(idR+1)) / 2
      (vPosSynth(idC) + vPosSynth(idC+1)) / 2]);

    insideInput = D1(center(1), center(2)) > ( stepSize / 2 - mgn);
    insideSymbol =  (D2(center(1), center(2)) < ( stepSize / 2 - mgn)) && (D1(center(1), center(2)) < ( stepSize / 2 - mgn));

    if insideInput
      fieldTypes(idR,idC)= 1;
    endif
    if insideSymbol
      fieldTypes(idR,idC)= 2;
    endif
  endfor
endfor

figure
subplot(2,2,1)
imagesc(M);

subplot(2,2,2)
imagesc(D1);
title("Distance to background, hiligthing input fields as max")

subplot(2,2,3)
imagesc(D2, [0 stepSize/2] );
title("Distance to boxes, real background have values >= gridSize/2 in center grid positions")

subplot(2,2,4)
imagesc(fieldTypes);
title("Classification of grid, 0=background, 1=input, 2=symbol or operator")

