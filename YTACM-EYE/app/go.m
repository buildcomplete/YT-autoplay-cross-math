pkg load signal

img = rgb2gray(imread('let.png'));

% Find playing area
edgeMinStrength = 20;
horzEdgeT = abs(conv2( img, [1 1 1; 0 0 0; -1 -1 -1], shape="same")) > edgeMinStrength;

figure
subplot(1,4,1)
title("original, grayscale")
imagesc(img)
colormap gray

subplot(1,4,2)
title("thresholded horizontal edges")
imagesc(horzEdgeT)
colormap gray

subplot(1,4,3)
title("Center profile of horizontal edges")
wh = size(horzEdgeT, 2)/2;
plot(horzEdgeT(:, wh), 1:size(horzEdgeT,1))
axis("ij")
ylim([0 size(horzEdgeT,1)]);

% Calculate playing field bondaries and varaible bondaries
horzCount = conv2( horzEdgeT, ones(1, size( horzEdgeT,2)), shape="valid") / size( horzEdgeT,2);
horzCount = conv( horzCount, [1 1 1 1 1]./5, shape="same" );

subplot(1,4,4)
title("smoothed, row sum of edges")
plot(horzCount, 1:size(horzEdgeT,1))
axis("ij")
ylim([0 size(horzEdgeT,1)])
[peak, loc] = findpeaks(horzCount, "MinPeakHeight", 0.8, "MinPeakDistance", 5);

% Mark regions in original image to validate
subplot(1,4,1)
hold on
plot( ones(length(loc), 1) .* wh, loc, "r_")

% extract playfield and variables
playfield = img(loc(1):loc(2), :);
variables = img(loc(3):loc(4), :);

figure
subplot(1,2,1);
imshow(playfield)
subplot(1,2,2);
imshow(variables)

% calculate grid
threshGrid = 100;
F_w = 11;
F = [ ones(1, F_w);  zeros(1, F_w);  ones(1, F_w) .* -1];

horzEdgePlayfield = abs(conv2( playfield, F, shape="same")) > threshGrid ;
horzCountPF = conv2( horzEdgePlayfield, ones(1, size( horzEdgePlayfield,2)), shape="valid") / size( horzEdgePlayfield,2);
horzCountPF = conv( horzCountPF, [1 1 1 1 1]./5, shape="same" );

figure
subplot(1,3,1);
imagesc(playfield)
subplot(1,3,2)
imagesc(horzEdgePlayfield );
subplot(1,3,3)
plot(horzCountPF, 1:length(horzCountPF));
axis("ij")
ylim( [0, length(horzEdgePlayfield)]);




