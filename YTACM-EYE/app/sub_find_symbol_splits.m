% Calculate symbol row and column indexes,
% if there are multiple symbols on the line
% each row of symColIdx will have that index
 function [symColIdx symRowIdx]= sub_find_symbol_splits(X)
  % Split image symbols, symbols are split if there is a vertical line between the symbols
  % Assuming first pixel is background
  maskBg = (abs(double(X) - double(X(1))) < 5) ./ (size(X,1));
  sProf = sum(maskBg,1);
  symbolIdx = sProf < ((max(sProf) - 0.01));

  % Symbol starting points > 0
  % Symbol end points < 0
  symbolIdx = conv(symbolIdx, [1 -1], shape="same");
  symStart = find(symbolIdx > 0.5, 3) + 1;
  symEnd = find(symbolIdx < -0.5, 3) + 1;
  symColIdx = [symStart; symEnd]'; % Each row now has column indexes of the symbol

  % top and bottom, since there are not multiple symbols,
  % i dont convolve and just use find
  sProf2 = sum(maskBg,2);
  symbolIdTB = sProf2 < ((max(sProf2) - 0.01));

  % I add some padding here to help minus not to be confused with equals
  symRowIdx =  [ find(symbolIdTB,1) - 3 find(symbolIdTB, 1, "last") + 3];

##  subplot(3,2,1);
##  imagesc(maskBg);
##
##  subplot(3,2,3);
##  plot(sProf)
##
##  subplot(3,2,5);
##  plot(symbolIdx)
##
##    subplot(3,2,4)
##  plot(sProf2)
##
##  subplot(3,2,6)
##  plot(symbolIdTB)

end

