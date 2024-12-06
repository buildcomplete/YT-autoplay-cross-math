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

[_, idxCols] = findpeaks(transCols, "MinPeakHeight", size(img,1)*0.6, "MinPeakDistance", 5);
[_, idxRows] = findpeaks(transRows, "MinPeakHeight", size(img,2)*0.8, "MinPeakDistance", 5);
idxRows= idxRows(2:end); % For rows we skip the first item (transition from info to bg)

if plotOn
  figure
  subplot(2,2,1);
  imagesc(maskOne)
  colormap gray
  hold on;
  plot( idxCols, ones(1,length(idxCols)) .* size(maskOne,1)/2 , 'r+');
  plot( ones(1,length(idxRows)) .* size(maskOne,2)/2, idxRows , 'g+');
  xticks(idxCols)
  yticks([idxRows(1) (idxRows(2)+idxRows(3))/2 idxRows(end-2)] )

  subplot(2,2,2);
  plot(transRows, 1:length(transRows));
  axis("ij");
  xlim([0 size(maskOne,2)]);
  ylim([0 size(maskOne,1)]);
  xticks(idxCols)
  yticks([idxRows(1) (idxRows(2)+idxRows(3))/2 idxRows(end-2)] )

  subplot(2,2,3);
  plot(transCols);
  axis("ij");
  xlim([0 size(maskOne,2)]);
  ylim([0 size(maskOne,1)]);
  xticks(idxCols)
  yticks([idxRows(1) (idxRows(2)+idxRows(3))/2 idxRows(end-2)] )
end

% Check if there was any borders on the sides,
% if not set the indexes to include all
if (length(idxCols) < 2)
  idxCols = [1 size(img,2)];
end

% extract playfield and variables
pad = 15;
playfield = img((idxRows(1)+pad):(idxRows(2)-pad), (idxCols(1)+pad:idxCols(2)-pad));
variables = img((idxRows(3)+pad):(idxRows(4)-pad), (idxCols(1)+pad):(idxCols(2)-pad));
p_b = [idxRows(1)+pad, idxCols(1)+pad ]; % Store offests for back projection
v_b = [idxRows(3)+pad, idxCols(1)+pad]; % Store offests for back projection
% Further more, remove top rows of playfield,
% Assuming there will
% 1) fist be background,
% 2) Then some rows with text (difficulty, time)
% 3) then background again
playfieldMask = (playfield - playfield(1)) < 5;
playfieldMaskCols = sum(playfieldMask,2) ;
varifieldMask = (variables - variables(1)) < 5;
varifieldMaskCols = sum(varifieldMask,2) ;

if plotOn
  figure;
  subplot(2,3,1);
  imagesc(playfieldMask)
  axis off
  subplot(2,3,2);
  plot( playfieldMaskCols, 1:length(playfieldMaskCols));
  axis("ij");
  axis off

  subplot(2,3,4);
  imagesc(varifieldMask)
  axis off
  subplot(2,3,5);
  plot( varifieldMaskCols, 1:length(varifieldMaskCols));
  axis("ij");
  axis off
end

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
p_b(1) = p_b(1)+i; % update offest for back projection

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

if plotOn
  subplot(2,3,3);
  imshow(playfield)
  subplot(2,3,6);
  imshow(variables)
end
