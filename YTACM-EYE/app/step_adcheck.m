pkg load signal;
pkg load image;

% Check add state

if nargin == 3
    arg_list = argv ();
    imageFilenameA = arg_list{1};
    resultFilename = arg_list{2};
    plotOn = arg_list{3} == "1";
else
    imageFilenameA = '../../shared/test_data/cut_scenes/ad_trans_x5.png';
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



XA_white = rgb2gray(XA) > 180; # Old method, works with white on black
XAbingrad = binGradX(XA, 20); # new method to detect white on white using gradient
R_x1 = xcorr2(XA_white, T_x1, "coeff");
R_x2 = xcorr2(XA_white, T_x2, "coeff");
R_x3g = xcorr2(XAbingrad, T_x3g, "coeff");
R_a1 = xcorr2(XA_white, T_a1, "coeff");
R_a2 = xcorr2(XA_white, T_a2, "coeff");
R_a3g = xcorr2(XAbingrad, T_a3g, "coeff");
[val_x1, idx_x1] = max(R_x1(:));
[val_x2, idx_x2] = max(R_x2(:));
[val_x3, idx_x3] = max(R_x3g(:));
[val_a1, idx_a1] = max(R_a1(:));
[val_a2, idx_a2] = max(R_a2(:));
[val_a3, idx_a3] = max(R_a3g(:));


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

function saveHit(fhandle, name, idx, R, T)
   fprintf(fhandle, sprintf('%s\n', name));
   [r,c] = ind2sub(size(R), idx);
   [tr tc]=size(T);

  fprintf(fhandle, '%d %d\n', floor(r-tr/2), floor(c-tr/2));
end

fid = fopen (resultFilename, "w");

if (val_x1 > 0.99)
  saveHit(fid, "adv_next", idx_x1, R_x1, T_x1)
elseif (val_x2 > 0.85 )
  saveHit(fid, "adv_next", idx_x2, R_x2, T_x2)
elseif (val_x3 > 0.78 )
  saveHit(fid, "adv_next", idx_x3, R_x3g, T_x3g)
elseif (val_a1 > 0.95 )
  saveHit(fid, "adv_next", idx_a1, R_a1, T_a1)
elseif (val_a2 > 0.95 )
  saveHit(fid, "adv_next", idx_a2, R_a2, T_a2)
elseif (val_a3 > 0.80 )
  saveHit(fid, "adv_next", idx_a3, R_a3g, T_a3g)
elseif (pksBN >= 1 )
  disp("We have next level blue button")
  fprintf(fid, 'bluenext\n');
  fprintf(fid, '%d %d\n', locBN, size(XA,2)/2);
else
  fprintf(fid, 'none\n');
end
fclose (fid);


