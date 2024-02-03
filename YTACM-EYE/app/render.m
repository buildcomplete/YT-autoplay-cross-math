% Render swipes to image
% Should really be applied as swipes or clicks on the phone
% But for now I cannot install adb

if nargin == 3
    arg_list = argv ();

    imageFilename = arg_list{1};
    csvFilename = arg_list{2};
    resultPlotFilename = arg_list{3};

else
    imageFilename = 'images/difficult.png';
    csvFilename = 'swipes.csv';
    resultPlotFilename = 'render.png';
end

img = rgb2gray(imread(imageFilename));
swipes = csvread(csvFilename)(2:end,:);

close all
hold off;
 imshow(img)
axis("ij");
for swipe  = swipes'
  hold on;
  ##swipe = swipes(1,:)
  #plot([swipe(1) swipe(3)], [swipe(2) swipe(4)], "gx:")
  plot([swipe(2) swipe(4) ], [swipe(1) swipe(3) ])
  pause
end

