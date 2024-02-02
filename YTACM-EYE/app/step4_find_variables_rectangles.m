M1 = abs(double(variables(1)) - double(variables)) < 5;
D1 = bwdist(M1);

peakEnergyCol = max(D1);  % column energy
peakEnergyRow = max(D1'); % row energy
rectSize = max(peakEnergyRow ) * 2; % field size

[_ varColIdx] = findpeaks(peakEnergyCol,  "MinPeakHeight", rectSize/3, "MinPeakDistance", rectSize);  % column indexes
[_ varRowIdx] = findpeaks(peakEnergyRow,  "MinPeakHeight", rectSize/3, "MinPeakDistance", rectSize); % row indes

% Populate energy at center, if the energy is zero the is no variable in that area
varIndexEnergy = D1(varRowIdx, varColIdx);

if plotOn
  figure
  subplot(3,2,1)
  imshow(variables)
  title("Original image")

  subplot(3,2,3)
  imshow(M1)
  title("Binary")

  subplot(3,2,5)
  imshow(D1, [0 max(D1(:))]);
  title("Distance transform")

  subplot(3,2,2)
  plot(peakEnergyCol);
  title("Column peaks")
  hold on;
  plot(varColIdx, peakEnergyCol(varColIdx), "ro")

  subplot(3,2,4)
  plot(peakEnergyRow);
  title("Row peaks")
  hold on;
  plot(varRowIdx, peakEnergyRow(varRowIdx), "ro")
end

