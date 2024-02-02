pkg load signal;
pkg load image;

if nargin == 3
    arg_list = argv ();
    imageFilename = arg_list{1}
    resultFilename = arg_list{2}
    plotOn = arg_list{3} == "1"

else
    imageFilename = 'images/difficult.png';
    resultFilename = 'cross-math-scan-result.txt'
    plotOn = false
end

disp(imageFilename)

%img = rgb2gray(imread('images/Screenshot_20240106_134529_Cross Math.jpg'));
close all;
img = rgb2gray(imread(imageFilename));
step0_segment_areas

step1_find_playfield_method2
% vPosSynth= column index
% hPosSynth= row index

step2_classify_playfield_box_type
% fieldTypes, 0=bg, 1=input, 2= symbol or operator

##% Create training templates, can run after step2_classify_playfield_box_type
##%trainingSetname
##setName = "expert"
##training_extract_template_material

step3_classify_symbols_and_operators
% symbolsAtPositions contains symbols at the positions

step4_find_variables_rectangles
step5_classify_available_symbols
% variables_with_pos contains avaliable variables

step6_write_output






