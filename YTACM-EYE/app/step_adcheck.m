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
T_x1 = imread('cutscenes/adv_X.png');
T_a1 = imread('cutscenes/adv_arrow1.png');

XA_white = rgb2gray(XA) > 200;
R_x1 = xcorr2(XA_white, T_x1, "coeff");
R_a1 = xcorr2(XA_white, T_a1, "coeff");
[val_x, idx_x] = max(R_x1(:));
[val_a1, idx_a1] = max(R_a1(:));



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

function saveHit(fhandle, name, idx, R)
   fprintf(fhandle, sprintf('%s\n', name));
   [r,c] = ind2sub(size(R), idx)
  fprintf(fhandle, '%d %d\n', r, c);
end

fid = fopen (resultFilename, "w");

if (val_x > 0.99)
  saveHit(fid, "adv_next", idx_x, R_x1)
elseif (val_a1 > 0.99 )
  saveHit(fid, "adv_next", idx_a1, R_a1)
elseif (pksBN >= 1 )
  disp("We have next level blue button")
  fprintf(fid, 'bluenext\n');
  fprintf(fid, '%d %d\n', locBN, size(XA,2)/2);
else
  fprintf(fid, 'none\n');
end
fclose (fid);

% Check if we have

