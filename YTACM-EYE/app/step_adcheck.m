pkg load signal;
pkg load image;

% Check add state

if nargin == 3
    arg_list = argv ();
    imageFilenameA = arg_list{1};
    resultFilename = arg_list{2};
    plotOn = arg_list{3} == "1";
else
    imageFilenameA = '../../shared/ad_trans_x.png';
    resultFilename = 'adv_check.txt';
    plotOn = true;
end

disp(['Adv check A : ' imageFilenameA]);
XA = imread(imageFilenameA);

% Check if we have next level blue button
targetBlue = [92, 131, 228];
DIST = sqrt((double(XA(:,:,1)) - targetBlue(1)).^2 + (double(XA(:,:,2)) - targetBlue(2)).^2 + (double(XA(:,:,3)) - targetBlue(3)).^2);
BR = medfilt1(mean(DIST<3,2)>0.5,31) ;
BR = conv(BR, ones(11,1)./11);
BR = conv(BR, ones(11,1)./11);
BR = conv(BR, ones(11,1)./11);
BR = conv(BR, ones(11,1)./11);
BR = conv(BR, ones(11,1)./11);
[pksBN, locBN, extra] = findpeaks(BR, "MinPeakHeight", 0.9, "MinPeakWidth", 100);

fid = fopen (resultFilename, "w");

if (pksBN >= 1 )
  disp("We have next level blue button")
  fprintf(fid, 'bluenext\n');
  fprintf(fid, '%d %d\n', locBN, size(XA,2)/2);
else
  fprintf(fid, 'none\n');
end
fclose (fid);

% Check if we have

