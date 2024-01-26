X = playfield;
M = abs(X-X(1) < 3);
D = bwdist(M);

% Size of box is max in the distance image
gridStepSize = 2 * max(D(:));

% grid start and stop position are first dips in mask (as mask is background)
boundarieR = sum(M,2); bLim = max(boundarieR) - gridStepSize/3;
boundsRows = sub_findFirstAndLast(boundarieR < bLim );
boundarieC = sum(M,1); bLim = max(boundarieC) - gridStepSize/3;
boundsCols = sub_findFirstAndLast(boundarieC < bLim );

% Create synthetics boundary vectors
nObj = floor([
  (boundsRows(2) - boundsRows(1) ) / gridStepSize
  (boundsCols(2) - boundsCols(1) ) / gridStepSize ]);

% Add one to number of objects since it is the edge boundaries wich is nBoxes + 1
vPosSynth = round(linspace(boundsCols(1), boundsCols(2), nObj(2) + 1)); % column index
hPosSynth = round(linspace(boundsRows(1), boundsRows(2), nObj(1) + 1)); % row index


figure
subplot(2,2,1)
colormap gray
imagesc(X);
hold on;
plot(ones(1,length(hPosSynth)) .* boundsCols(1), hPosSynth, 'r+');
plot(vPosSynth, ones(1,length(vPosSynth)) .* boundsRows(1), 'g+');


subplot(2,2,2)
imagesc(M);
subplot(2,2,3)
imagesc(D);
