% Sample sidecolor to use as mask
bgColor = img(size(img,1), 3);
maskOne = ((img - bgColor) < 5) .* 1; % create mask with same value as border
maskOne = imopen( maskOne, ones(9)); % Clean out noise from mask using open

% Project mask
sumCols = sum(maskOne, 1);
sumRows = sum(maskOne, 2);

% detect transitions (To avoid hand writing loops)
transCols = abs(conv(sumCols, [1 0 -1], shape="same" ));
transCols(1)=0;transCols(end)=0; % fix borders
transRows = abs(conv(sumRows, [1 0 -1], shape="same" ));
transRows(1)=0;transRows(end)=0; % fix borders

[_, idxCols] = findpeaks(transCols, "MinPeakHeight", 100, "MinPeakDistance", 5);
[_, idxRows] = findpeaks(transRows, "MinPeakHeight", 100, "MinPeakDistance", 5);
idxRows= idxRows(2:end); % For rows we skip the first item (transition from info to bg)

figure
subplot(2,2,1);
imagesc(maskOne)
colormap gray
hold on;
plot( idxCols, ones(1,length(idxCols)) .* size(maskOne,1)/2 , 'r+');
plot( ones(1,length(idxRows)) .* size(maskOne,2)/2, idxRows , 'g+');

subplot(2,2,2);
plot(transRows, 1:length(transRows));
axis("ij");

subplot(2,2,3);
plot(transCols);

% extract playfield and variables
pad = 15;
playfield = img((idxRows(1)+pad):(idxRows(2)-pad), (idxCols(1)+pad:idxCols(2)-pad));
variables = img((idxRows(3)+pad):(idxRows(4)-pad), (idxCols(1)+pad):(idxCols(2)-pad));

% Further more, remove top rows of playfield,
% Assuming there will
% 1) fist be background,
% 2) Then some rows with text (difficulty, time)
% 3) then background again
playfieldMask = (playfield - playfield(1)) < 5;
playfieldMaskCols = sum(playfieldMask,2) ;
varifieldMask = (variables - variables(1)) < 5;
varifieldMaskCols = sum(varifieldMask,2) ;


figure;
subplot(2,2,1);
imagesc(playfieldMask)
subplot(2,2,2);
plot( playfieldMaskCols, 1:length(playfieldMaskCols));
axis("ij");

subplot(2,2,3);
imagesc(varifieldMask)
subplot(2,2,4);
plot( varifieldMaskCols, 1:length(varifieldMaskCols));
axis("ij");

foundDip = false;
for i=2:length(playfieldMaskCols)
  if (!foundDip)
    foundDip = playfieldMaskCols(i) < (size(playfieldMask,2) - 1);
  end

  if (foundDip && playfieldMaskCols(i) == size(playfieldMask,2))
    break;
  end
end
playfield=playfield(i:end,:);

foundDip = false;
for i=length(varifieldMaskCols):-1:2
  if (!foundDip)
    foundDip = varifieldMaskCols(i) < (size(varifieldMask,2) - 1);
  end

  if (foundDip && varifieldMaskCols(i) == size(varifieldMask,2))
    break;
  end
end
variables=variables(1:i,:);


figure
subplot(1,2,1);
imshow(playfield)
subplot(1,2,2);
imshow(variables)


