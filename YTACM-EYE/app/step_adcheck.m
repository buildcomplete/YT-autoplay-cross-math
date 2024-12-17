pkg load signal;
pkg load image;

% Check add state

if nargin == 3
    arg_list = argv ();
    imageFilenameA = arg_list{1};
    resultFilename = arg_list{2};
    plotOn = arg_list{3} == "1";
else
    imageFilenameA = '../../shared/test_data/cut_scenes/ad_trans_x.png';
    resultFilename = 'adv_check.txt';
    plotOn = true;
end

function bg = binGradX(X, t)
  if (size(X,3)==3)
    Xg = rgb2gray(X);
  else
    Xg = X;
  end
  dx = conv2(Xg, [1 0 -1],'same');
  dy = conv2(Xg, [1 0 -1]', 'same');
  bg = sqrt(dx.^2 + dy.^2) > t;
end

XA = imread(imageFilenameA);
T_x1 = imread('cutscenes/adv_X.png');
T_x2 = imread('cutscenes/adv_X2.png');
T_x3g = imread('cutscenes/adv_X3_grad.png');
T_a1 = imread('cutscenes/adv_arrow1.png');
T_a2 = imread('cutscenes/adv_arrow2.png');
T_a3g = binGradX(T_a2, 0.5);

function [eMax r c] = symbolMaxInRoi(X, T, r1,c1, r2, c2)
  R = xcorr2(X(r1:r2,c1:c2), T, "coeff");
  [eMax, idx] = max(R(:));
  [r,c] = ind2sub(size(R), idx);
  r = floor(r-size(T,1)/2)+r1;
  c = floor(c-size(T,2)/2)+c1;
end

XA_white = rgb2gray(XA) > 180; # Old method, works with white on black
XAbingrad = binGradX(XA, 20); # new method to detect white on white using gradient

[val_x1, r_x1, c_x1] = symbolMaxInRoi(XA_white, T_x1, 50, 1, 250, size(XA_white,2));
[val_x2, r_x2, c_x2] = symbolMaxInRoi(XA_white, T_x2, 50, 1, 250, size(XA_white,2));
[val_x3, r_x3, c_x3] = symbolMaxInRoi(XAbingrad, T_x3g, 50, 1, 250, size(XA_white,2));
[val_a1, r_a1, c_a1] = symbolMaxInRoi(XA_white, T_a1, 50, 1, 250, size(XA_white,2));
[val_a2, r_a2, c_a2] = symbolMaxInRoi(XA_white, T_a2, 50, 1, 250, size(XA_white,2));
[val_a3, r_a3, c_a3] = symbolMaxInRoi(XAbingrad, T_a3g, 50, 1, 250, size(XA_white,2));

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

function saveHit2(fhandle, name, r,c)
  fprintf(fhandle, sprintf('%s\n', name));
  fprintf(fhandle, '%d %d\n', r, c);
end

fid = fopen (resultFilename, "w");

if (val_x1 > 0.99)
  saveHit2(fid, "adv_next", r_x1, c_x1);
elseif (val_x2 > 0.85 )
  saveHit2(fid, "adv_next", r_x2, c_x2);
elseif (val_x3 > 0.78 )
  saveHit2(fid, "adv_next", r_x3, c_x3);
elseif (val_a1 > 0.95 )
  saveHit2(fid, "adv_next", r_a1, c_a1);
elseif (val_a2 > 0.95 )
  saveHit2(fid, "adv_next", r_a2, c_a2);
elseif (val_a3 > 0.80 )
  saveHit2(fid, "adv_next", r_a3, c_a3);
elseif (pksBN >= 1 )
  disp("We have next level blue button")
  fprintf(fid, 'bluenext\n');
  fprintf(fid, '%d %d\n', locBN, size(XA,2)/2);
else
  fprintf(fid, 'none\n');
end
fclose (fid);


