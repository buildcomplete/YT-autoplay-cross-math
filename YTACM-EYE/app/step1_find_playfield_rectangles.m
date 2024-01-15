% Assuming 'playfield' is set to a grayscale image just containing the rectangles
X = playfield;

F = [ 1 1 1 1 1 ; 0 0 0 0 0; -1 -1 -1 -1 -1];
edgesIH = abs(conv2(abs(X-X(1)) < 2, F, shape="same") ) > 1;
edgesIV = abs(conv2(abs(X-X(1)) < 2, F', shape="same") ) > 1;

% Project and detect sharp edges to reduce signal from numbers
pV = abs(conv(sum(edgesIV,1), [1 0 -1], shape="same"));
pH = abs(conv(sum(edgesIH,2), [1 0 -1], shape="same"));

% Apply gausian smoothing to further reduce noise and double pulse from lines
pV = conv(pV, gaussian(15, 0.25), shape="same");
pH = conv(pH, gaussian(15, 0.25), shape="same");

% Remove false signal from border
marg = 21;
pV(1:marg)=0; pH(1:marg)=0;
pV((end-marg):end)=0; pH((end-marg):end)=0;

% Find peaks as usual
[_ vPos] = findpeaks(pV, "MinPeakHeight", 450, "MinPeakDistance", 30);
[_ hPos] = findpeaks(pH, "MinPeakHeight", 450, "MinPeakDistance", 30);

% Remove false positives or misses using median point distance
% Notice the items should be fairly rectangular
% I also assume first and last point is correct, this is not to bad an assumptions since
objectSize = [median(conv(hPos', [1 -1], shape="valid")) median(conv(vPos, [1 -1], shape="valid"))];
objectSizeM = max(objectSize)


% createGrid.
nStepV = round((vPos(end)-vPos(1))/objectSizeM);
nStepH = round((hPos(end)-hPos(1))/objectSizeM);
vPosSynth = linspace(vPos(1), vPos(end), nStepV+1); % column index
hPosSynth = linspace(hPos(1), hPos(end), nStepH+1); % row index

figure
subplot(2,2,1)
imagesc(edgesIH);
title('horizontal: row edges')

subplot(2,2,2)
imagesc(edgesIV);
title('vertical: column edges')

subplot(2,2,3)
plot(pH)
title('row edges transitions')

subplot(2,2,4)
plot(pV)
title('column edges transitions')


figure
imagesc(X);
title("image including first estimate of lines and refined estimate")
colormap gray
hold on;
plot(ones(1,length(hPos)), hPos, 'r+')
plot(vPos, ones(1,length(vPos)), 'g+')
plot(ones(1,length(hPosSynth)) .* vPos(1), hPosSynth, 'r_')
plot(vPosSynth, ones(1,length(vPosSynth)) .* hPos(1), 'g|')
