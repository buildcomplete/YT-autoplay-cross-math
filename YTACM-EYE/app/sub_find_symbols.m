function symbolIdx = sub_find_symbols(I, symbolLib)
  [symColIdx symRowIdx] = sub_find_symbol_splits(I);

  nSym = size(symColIdx,1);
  symbolIdx = zeros(nSym,1);
  symbolMaxes = zeros(nSym,1);

  for sId = 1:length(symbolLib)
    T = symbolLib{sId};
    aspectOk = true;

    % scale symbol to be same height as detected image,
    % notice a padding was origiginally added
    % somehow we have to respected that
    % respect!
    if (nSym == 1 ) %% If there is only one symbol, scale to exact size of symbol
      bboxT = size(T)-6;
      bboxI = ([symRowIdx(2)- symRowIdx(1), symColIdx(2) - symColIdx(1)]-6);
      arT = bboxT(1) / bboxT(2);
      arI = bboxI(1) / bboxI(2);

      # Warning, there is something fishy about the logic since a padding is added to the template
      # If the image is much smaller, the padding will be relatively bigger
      # and impact aspect ratio
      # The aspect ratio goes toward 1 as image size goes towards 0
      # Still a bit puzzled, since I do remove the padding in the comparison
      aspectOk = (max([arT arI]) / min([arT arI])) < 1.25; % Aspect ratio of symbol must be similar%
      T_Diag = sqrt(sum(bboxT.^2));
      I_Diag = sqrt(sum(bboxI.^2));
      scaleFactor = I_Diag / T_Diag;

    else  % If multiple symbols (numbers), all can be scaled according to height
      q=size(T,1)-6;
      scaleFactor =  (symRowIdx(2)-symRowIdx(1)-6) / (q);
    endif

    if not(aspectOk)
      energy = zeros(size(I));
    else

      % Limit scalins, so '1' and '7' doesn look like '-'
      %scaleFactor = min([1.1 max([0.9 scaleFactor])]);
      T = imresize(double(T), scaleFactor, "bicubic");

      energy = xcorr2(I, T, "coeff");
      energy = imsmooth(energy, "Gaussian");
      % padding was applied, remove this from result
      crap =  floor((size(energy) - size(I)) ./ 2);
      energy = energy(crap(1):(size(I,1)+crap(1)), crap(2):(size(I,2)+crap(2)));
    endif

    cR = floor(mean(symRowIdx));
    energyProfileCenter = max(energy((cR-2):(cR+2),:));
    for sId2 = 1:nSym
      newEnergy = max(energyProfileCenter(:,symColIdx(sId2,1):symColIdx(sId2,2)));
      if (newEnergy > symbolMaxes(sId2))
        symbolMaxes(sId2) = newEnergy;
        symbolIdx(sId2) = sId;
      endif
    endfor
  endfor
end
