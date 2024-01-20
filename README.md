# YT-autoplay-cross-math

A bot to play cross math.
The system consist of 3  individual component

1. A image analyzer that recognizes the game elements from a image.
2. A solver that calculates a solution for solving the puzzle
3. Last something that can apply the above two components to the game running on a phone.

# The game
The game itself is a math puzzle where you need to solve some equations. Below is sample 4 frames from the game at the possible difficulties used to create the image recognizer

```matlab
figure; 
subplot(1,4,1); imshow(imread('images/easy.jpg')); title('Easy');
subplot(1,4,2); imshow(imread('images/medium.jpg')); title('Medium');
subplot(1,4,3); imshow(imread('images/hard.jpg')); title('Hard');
subplot(1,4,4); imshow(imread('images/expert.png')); title('Expert');
print("game-example.png")
```
![Example screenshots used for creating the image recognizer](./YTACM-EYE/doc/game-example.png)

# Image recognizer
The image recognizer takes an image and spits out the data needed to analyze
- The image solver is made using Octave.
- The templates are created with Octave itself.
- No values was read outside octave, such as colors or positions.

The sequence is the following
```mermaid
flowchart LR
Step0(Detect top and bottom)-->Step0_2(Refine by removing text and circles)-->TopGridDetect(Find top Grid)-->TopGridClassify(Classify Top grid)-->TopGridRecognize(Read symbols and operators)
Step0_2-->DetectBottomGrid(Find bottom Grid)-->ReadSymbols(Read symbols)
```

## [step0_segment_areas.m](./YTACM-EYE/app/step0_segment_areas.m)
### Detect top and bottom:
![Detect top and bottom](./YTACM-EYE/doc/step0_fig1.png)
### Refine by removing text and circles 
![Detect top and bottom](./YTACM-EYE/doc/step0_fig2.png)
![Detect top and bottom](./YTACM-EYE/doc/step0_fig3.png)

## [step1_find_playfield_method2.m](./YTACM-EYE/app/step1_find_playfield_method2.m)
### Find top grid
![Detect top and bottom](./YTACM-EYE/doc/step1_fig1.png)

## [step2_classify_playfield_box_type.m](./YTACM-EYE/app/step2_classify_playfield_box_type.m)
![Classify grid](./YTACM-EYE/doc/step2_fig1.png)

## [step3_classify_symbols_and_operators.m](./YTACM-EYE/app/step3_classify_symbols_and_operators.m)
This was the most difficult part to get working robustly, in each field we have to find the symbols and combine into a number, I do that by taking the maxim correlation inside each separate region in the field. Response sample below after some filtering to remove mismatches.

- Detection of the symbol '1'
![Detection of the number one](./YTACM-EYE/doc/xcor_7_9.png)
- Detection of the two symbols '1' and '4' inside in field
![Detection of the number 14](./YTACM-EYE/doc/xcor_5_1.png)

## [step4_find_variables_rectangles.m](./YTACM-EYE/app/step4_find_variables_rectangles.m)
Detect grid, the detection here, based on a distance transform is super simple. (Most of the code in the file is plotting)
![Detection of the number 14](./YTACM-EYE/doc/step4_fig1.png)

## [step5_classify_available_symbols.m](./YTACM-EYE/app/step5_classify_available_symbols.m)
Classify using same logic as as in step3.

The following is the output
- fieldTypes, 0=bg, 1=input, 2= symbol or operator

Example from using the image 'Easy', the following output is generated (The format is quite verbose but should be readable)

```text
fieldTypes=
   11    6
   0   1   2   2   2   1
   0   0   0   2   0   0
   0   2   0   1   0   0
   2   2   1   2   2   0
   0   2   0   2   0   0
   0   2   0   0   0   0
   0   1   2   1   2   2
   0   0   0   2   0   0
   0   1   2   2   2   2
   0   0   0   2   0   0
   0   0   0   1   0   0
symbolsAtPositions=
21
1,3:+ 
1,4:9 
1,5:= 
2,4:+ 
3,2:22
4,1:3 
4,2:+ 
4,4:= 
4,5:7 
5,2:5 
5,4:27
6,2:= 
7,3:- 
7,5:= 
7,6:2 
8,4:+ 
9,3:+ 
9,4:4 
9,5:= 
9,6:6 
10,4:=
variables_with_pos=
8
1,1:18
1,2:18
1,3:25
1,4:9 
1,5:4 
2,1:29
2,2:2 
2,3:27
```

# Brain
The brain is used to solve the puzzle, 

- Step1, load data
- Step2, detect equations in the matrix (they are just numbers)
- Step3, Map variables in equations to coordinate system
- Set variables and test for validity, select equations according to lowest level of freedom to limit test space

## Solution for easy
 ```time  python solve.py /shared/cross-math-scan-result.txt```
```text
Solution:
[('9+9=18', set()), ('3+4=7', set()), ('27-25=2', set()), ('2+4=6', set()), ('22+5=27', set()), ('9+18=27', set()), ('25+4=29', set())]
{'varname': (0, 5), 'value': '18', 'symIdx': '1,2'}
{'varname': (0, 1), 'value': '9', 'symIdx': '1,4'}
{'varname': (10, 3), 'value': '29', 'symIdx': '2,1'}
{'varname': (2, 3), 'value': '18', 'symIdx': '1,1'}
{'varname': (6, 3), 'value': '25', 'symIdx': '1,3'}
{'varname': (6, 1), 'value': '27', 'symIdx': '2,3'}
{'varname': (8, 1), 'value': '2', 'symIdx': '2,2'}
{'varname': (3, 2), 'value': '4', 'symIdx': '1,5'}

real    0m0.067s
user    0m0.015s
sys     0m0.023s
```

The following diagram shows the path traversed to find the solution
```mermaid
flowchart TD
root-->2_3_2_18
2_3_2_18-->root
root-->2_3_2_25
2_3_2_25-->root
root-->2_3_2_9
2_3_2_9-->root
root-->2_3_2_4
2_3_2_4-->3_8_1_18
3_8_1_18-->2_3_2_4
2_3_2_4-->3_8_1_25
3_8_1_25-->2_3_2_4
2_3_2_4-->3_8_1_9
3_8_1_9-->2_3_2_4
2_3_2_4-->3_8_1_29
3_8_1_29-->2_3_2_4
2_3_2_4-->3_8_1_2
3_8_1_2-->4_6_1_18
4_6_1_18-->3_8_1_2
3_8_1_2-->4_6_1_25
4_6_1_25-->3_8_1_2
3_8_1_2-->4_6_1_9
4_6_1_9-->3_8_1_2
3_8_1_2-->4_6_1_29
4_6_1_29-->3_8_1_2
3_8_1_2-->4_6_1_27
4_6_1_27-->5_6_3_18
5_6_3_18-->4_6_1_27
4_6_1_27-->5_6_3_25
5_6_3_25-->6_2_3_18
6_2_3_18-->7_10_3_18
7_10_3_18-->6_2_3_18
6_2_3_18-->7_10_3_9
7_10_3_9-->6_2_3_18
6_2_3_18-->7_10_3_29
7_10_3_29-->8_0_1_18
8_0_1_18-->9_0_5_9
9_0_5_9-->8_0_1_18
8_0_1_18-->7_10_3_29
7_10_3_29-->8_0_1_9
8_0_1_9-->9_0_5_18-->Done
```

## Solution for medium
```text
Solution:
[('21/3=7', set()), ('18/2=9', set()), ('6+16=22', set()), ('47+19=66', set()), ('14-11=3', set()), ('10+9=19', set()), ('83-27=56', set()), ('23+30=53', set()), ('21+26=47', set()), ('19+8=27', set()), ('23-7=16', set()), ('66-10=56', set()), ('40-18=22', set()), ('11+19=30', set()), ('9-6=3', set())]   
{'varname': (4, 10), 'value': '6', 'symIdx': '2,5'}
{'varname': (4, 2), 'value': '6', 'symIdx': '1,5'}
{'varname': (4, 6), 'value': '22', 'symIdx': '3,2'}
{'varname': (2, 6), 'value': '18', 'symIdx': '2,1'}
{'varname': (2, 10), 'value': '9', 'symIdx': '3,4'}
{'varname': (4, 4), 'value': '16', 'symIdx': '3,3'}
{'varname': (8, 2), 'value': '8', 'symIdx': '2,4'}
{'varname': (2, 2), 'value': '3', 'symIdx': '2,3'}
{'varname': (2, 0), 'value': '21', 'symIdx': '3,1'}
{'varname': (10, 8), 'value': '30', 'symIdx': '1,4'}
{'varname': (10, 4), 'value': '56', 'symIdx': '1,3'}
{'varname': (8, 4), 'value': '10', 'symIdx': '1,1'}
{'varname': (6, 10), 'value': '3', 'symIdx': '1,2'}
{'varname': (6, 4), 'value': '66', 'symIdx': '2,2'}

real    0m0.086s
user    0m0.036s
sys     0m0.024s
```

```mermaid
flowchart TD
root-->2_6_4_10
2_6_4_10-->root
root-->2_6_4_3
2_6_4_3-->root
root-->2_6_4_56
2_6_4_56-->root
root-->2_6_4_30
2_6_4_30-->root
root-->2_6_4_6
2_6_4_6-->root
root-->2_6_4_18
2_6_4_18-->root
root-->2_6_4_66
2_6_4_66-->3_6_10_10
3_6_10_10-->2_6_4_66
2_6_4_66-->3_6_10_3
3_6_10_3-->4_8_4_10
4_8_4_10-->5_10_4_56
5_10_4_56-->6_10_8_30
6_10_8_30-->7_2_0_6
7_2_0_6-->6_10_8_30
6_10_8_30-->7_2_0_18
7_2_0_18-->6_10_8_30
6_10_8_30-->7_2_0_3
7_2_0_3-->6_10_8_30
6_10_8_30-->7_2_0_8
7_2_0_8-->6_10_8_30
6_10_8_30-->7_2_0_21
7_2_0_21-->8_2_2_6
8_2_2_6-->7_2_0_21
7_2_0_21-->8_2_2_18
8_2_2_18-->7_2_0_21
7_2_0_21-->8_2_2_3
8_2_2_3-->9_8_2_6
9_8_2_6-->8_2_2_3
8_2_2_3-->9_8_2_18
9_8_2_18-->8_2_2_3
8_2_2_3-->9_8_2_8
9_8_2_8-->10_4_4_6
10_4_4_6-->9_8_2_8
9_8_2_8-->10_4_4_18
10_4_4_18-->9_8_2_8
9_8_2_8-->10_4_4_22
10_4_4_22-->9_8_2_8
9_8_2_8-->10_4_4_16
10_4_4_16-->11_2_10_6
11_2_10_6-->12_2_6_18
12_2_6_18-->11_2_10_6
11_2_10_6-->12_2_6_6
12_2_6_6-->11_2_10_6
11_2_10_6-->12_2_6_22
12_2_6_22-->11_2_10_6
11_2_10_6-->12_2_6_9
12_2_6_9-->11_2_10_6
11_2_10_6-->10_4_4_16
10_4_4_16-->11_2_10_18
11_2_10_18-->12_2_6_6
12_2_6_6-->11_2_10_18
11_2_10_18-->12_2_6_22
12_2_6_22-->11_2_10_18
11_2_10_18-->12_2_6_9
12_2_6_9-->11_2_10_18
11_2_10_18-->10_4_4_16
10_4_4_16-->11_2_10_22
11_2_10_22-->12_2_6_6
12_2_6_6-->11_2_10_22
11_2_10_22-->12_2_6_18
12_2_6_18-->11_2_10_22
11_2_10_22-->12_2_6_9
12_2_6_9-->11_2_10_22
11_2_10_22-->10_4_4_16
10_4_4_16-->11_2_10_9
11_2_10_9-->12_2_6_6
12_2_6_6-->11_2_10_9
11_2_10_9-->12_2_6_18
12_2_6_18-->13_4_6_6
13_4_6_6-->12_2_6_18
12_2_6_18-->13_4_6_22
13_4_6_22-->14_4_2_6
14_4_2_6-->15_4_10_6-->Done
```

## Solution for difficult
```text
Solution:
[('21/3=7', set()), ('18/2=9', set()), ('6+16=22', set()), ('47+19=66', set()), ('14-11=3', set()), ('10+9=19', set()), ('83-27=56', set()), ('23+30=53', set()), ('21+26=47', set()), ('19+8=27', set()), ('23-7=16', set()), ('66-10=56', set()), ('40-18=22', set()), ('11+19=30', set()), ('9-6=3', set())]   
{'varname': (4, 10), 'value': '6', 'symIdx': '2,5'}
{'varname': (4, 2), 'value': '6', 'symIdx': '1,5'}
{'varname': (4, 6), 'value': '22', 'symIdx': '3,2'}
{'varname': (2, 6), 'value': '18', 'symIdx': '2,1'}
{'varname': (2, 10), 'value': '9', 'symIdx': '3,4'}
{'varname': (4, 4), 'value': '16', 'symIdx': '3,3'}
{'varname': (8, 2), 'value': '8', 'symIdx': '2,4'}
{'varname': (2, 2), 'value': '3', 'symIdx': '2,3'}
{'varname': (2, 0), 'value': '21', 'symIdx': '3,1'}
{'varname': (10, 8), 'value': '30', 'symIdx': '1,4'}
{'varname': (10, 4), 'value': '56', 'symIdx': '1,3'}
{'varname': (8, 4), 'value': '10', 'symIdx': '1,1'}
{'varname': (6, 10), 'value': '3', 'symIdx': '1,2'}
{'varname': (6, 4), 'value': '66', 'symIdx': '2,2'}

real    0m0.076s
user    0m0.039s
sys     0m0.020s
```

```mermaid
flowchart
root-->2_6_4_10
2_6_4_10-->root
root-->2_6_4_3
2_6_4_3-->root
root-->2_6_4_56
2_6_4_56-->root
root-->2_6_4_30
2_6_4_30-->root
root-->2_6_4_6
2_6_4_6-->root
root-->2_6_4_18
2_6_4_18-->root
root-->2_6_4_66
2_6_4_66-->3_6_10_10
3_6_10_10-->2_6_4_66
2_6_4_66-->3_6_10_3
3_6_10_3-->4_8_4_10
4_8_4_10-->5_10_4_56
5_10_4_56-->6_10_8_30
6_10_8_30-->7_2_0_6
7_2_0_6-->6_10_8_30
6_10_8_30-->7_2_0_18
7_2_0_18-->6_10_8_30
6_10_8_30-->7_2_0_3
7_2_0_3-->6_10_8_30
6_10_8_30-->7_2_0_8
7_2_0_8-->6_10_8_30
6_10_8_30-->7_2_0_21
7_2_0_21-->8_2_2_6
8_2_2_6-->7_2_0_21
7_2_0_21-->8_2_2_18
8_2_2_18-->7_2_0_21
7_2_0_21-->8_2_2_3
8_2_2_3-->9_8_2_6
9_8_2_6-->8_2_2_3
8_2_2_3-->9_8_2_18
9_8_2_18-->8_2_2_3
8_2_2_3-->9_8_2_8
9_8_2_8-->10_4_4_6
10_4_4_6-->9_8_2_8
9_8_2_8-->10_4_4_18
10_4_4_18-->9_8_2_8
9_8_2_8-->10_4_4_22
10_4_4_22-->9_8_2_8
9_8_2_8-->10_4_4_16
10_4_4_16-->11_2_10_6
11_2_10_6-->12_2_6_18
12_2_6_18-->11_2_10_6
11_2_10_6-->12_2_6_6
12_2_6_6-->11_2_10_6
11_2_10_6-->12_2_6_22
12_2_6_22-->11_2_10_6
11_2_10_6-->12_2_6_9
12_2_6_9-->11_2_10_6
11_2_10_6-->10_4_4_16
10_4_4_16-->11_2_10_18
11_2_10_18-->12_2_6_6
12_2_6_6-->11_2_10_18
11_2_10_18-->12_2_6_22
12_2_6_22-->11_2_10_18
11_2_10_18-->12_2_6_9
12_2_6_9-->11_2_10_18
11_2_10_18-->10_4_4_16
10_4_4_16-->11_2_10_22
11_2_10_22-->12_2_6_6
12_2_6_6-->11_2_10_22
11_2_10_22-->12_2_6_18
12_2_6_18-->11_2_10_22
11_2_10_22-->12_2_6_9
12_2_6_9-->11_2_10_22
11_2_10_22-->10_4_4_16
10_4_4_16-->11_2_10_9
11_2_10_9-->12_2_6_6
12_2_6_6-->11_2_10_9
11_2_10_9-->12_2_6_18
12_2_6_18-->13_4_6_6
13_4_6_6-->12_2_6_18
12_2_6_18-->13_4_6_22
13_4_6_22-->14_4_2_6
14_4_2_6-->15_4_10_6-->Done

```

## Solution for expert
```text
Solution:
[('11-8=3', set()), ('4+2=6', set()), ('3-2=1', set()), ('21-6=15', set()), ('16-1=15', set()), ('16+7=23', set()), ('118-96=22', set()), ('39/13=3', set()), ('14+21=35', set()), ('11-8=3', set()), ('6x16=96', set()), ('8/4=2', set()), ('15+7=22', set()), ('3-2=1', set()), ('16+23=39', set()), ('6/6=1', set())]
{'varname': (10, 8), 'value': '13', 'symIdx': '1,6'}
{'varname': (10, 6), 'value': '39', 'symIdx': '3,4'}
{'varname': (8, 6), 'value': '23', 'symIdx': '3,3'}
{'varname': (8, 4), 'value': '7', 'symIdx': '2,5'}
{'varname': (8, 2), 'value': '16', 'symIdx': '3,1'}
{'varname': (10, 2), 'value': '96', 'symIdx': '2,4'}
{'varname': (10, 4), 'value': '22', 'symIdx': '3,5'}
{'varname': (6, 10), 'value': '15', 'symIdx': '2,1'}
{'varname': (6, 6), 'value': '16', 'symIdx': '1,2'}
{'varname': (4, 4), 'value': '2', 'symIdx': '1,5'}
{'varname': (4, 2), 'value': '3', 'symIdx': '3,6'}
{'varname': (0, 4), 'value': '8', 'symIdx': '2,6'}
{'varname': (0, 2), 'value': '11', 'symIdx': '1,3'}
{'varname': (4, 8), 'value': '6', 'symIdx': '3,2'}
{'varname': (0, 6), 'value': '3', 'symIdx': '2,3'}
{'varname': (2, 8), 'value': '6', 'symIdx': '2,2'}
{'varname': (2, 6), 'value': '2', 'symIdx': '1,4'}
{'varname': (6, 0), 'value': '21', 'symIdx': '1,1'}

real    0m0.161s
user    0m0.113s
sys     0m0.021s
```

```mermaid
flowchart
root-->2_6_0_21
2_6_0_21-->3_2_6_16
3_2_6_16-->4_2_8_11
4_2_8_11-->3_2_6_16
3_2_6_16-->4_2_8_2
4_2_8_2-->3_2_6_16
3_2_6_16-->4_2_8_13
4_2_8_13-->3_2_6_16
3_2_6_16-->4_2_8_15
4_2_8_15-->3_2_6_16
3_2_6_16-->4_2_8_6
4_2_8_6-->3_2_6_16
3_2_6_16-->4_2_8_3
4_2_8_3-->3_2_6_16
3_2_6_16-->4_2_8_96
4_2_8_96-->3_2_6_16
3_2_6_16-->4_2_8_7
4_2_8_7-->3_2_6_16
3_2_6_16-->4_2_8_8
4_2_8_8-->3_2_6_16
3_2_6_16-->4_2_8_16
4_2_8_16-->3_2_6_16
3_2_6_16-->4_2_8_23
4_2_8_23-->3_2_6_16
3_2_6_16-->4_2_8_39
4_2_8_39-->3_2_6_16
3_2_6_16-->4_2_8_22
4_2_8_22-->3_2_6_16
3_2_6_16-->2_6_0_21
2_6_0_21-->3_2_6_11
3_2_6_11-->4_2_8_16
4_2_8_16-->3_2_6_11
3_2_6_11-->4_2_8_2
4_2_8_2-->3_2_6_11
3_2_6_11-->4_2_8_13
4_2_8_13-->3_2_6_11
3_2_6_11-->4_2_8_15
4_2_8_15-->5_0_6_16
5_0_6_16-->4_2_8_15
4_2_8_15-->5_0_6_2
5_0_6_2-->4_2_8_15
4_2_8_15-->5_0_6_13
5_0_6_13-->4_2_8_15
4_2_8_15-->5_0_6_6
5_0_6_6-->4_2_8_15
4_2_8_15-->5_0_6_3
5_0_6_3-->4_2_8_15
4_2_8_15-->5_0_6_96
5_0_6_96-->4_2_8_15
4_2_8_15-->5_0_6_7
5_0_6_7-->4_2_8_15
4_2_8_15-->5_0_6_8
5_0_6_8-->4_2_8_15
4_2_8_15-->5_0_6_23
5_0_6_23-->4_2_8_15
4_2_8_15-->5_0_6_39
5_0_6_39-->4_2_8_15
4_2_8_15-->5_0_6_22
5_0_6_22-->4_2_8_15
4_2_8_15-->3_2_6_11
3_2_6_11-->4_2_8_6
4_2_8_6-->3_2_6_11
3_2_6_11-->4_2_8_3
4_2_8_3-->3_2_6_11
3_2_6_11-->4_2_8_96
4_2_8_96-->3_2_6_11
3_2_6_11-->4_2_8_7
4_2_8_7-->3_2_6_11
3_2_6_11-->4_2_8_8
4_2_8_8-->3_2_6_11
3_2_6_11-->4_2_8_23
4_2_8_23-->3_2_6_11
3_2_6_11-->4_2_8_39
4_2_8_39-->3_2_6_11
3_2_6_11-->4_2_8_22
4_2_8_22-->3_2_6_11
3_2_6_11-->2_6_0_21
2_6_0_21-->3_2_6_2
3_2_6_2-->4_2_8_16
4_2_8_16-->3_2_6_2
3_2_6_2-->4_2_8_11
4_2_8_11-->3_2_6_2
3_2_6_2-->4_2_8_2
4_2_8_2-->3_2_6_2
3_2_6_2-->4_2_8_13
4_2_8_13-->3_2_6_2
3_2_6_2-->4_2_8_15
4_2_8_15-->3_2_6_2
3_2_6_2-->4_2_8_6
4_2_8_6-->5_0_6_16
5_0_6_16-->4_2_8_6
4_2_8_6-->5_0_6_11
5_0_6_11-->4_2_8_6
4_2_8_6-->5_0_6_2
5_0_6_2-->4_2_8_6
4_2_8_6-->5_0_6_13
5_0_6_13-->4_2_8_6
4_2_8_6-->5_0_6_15
5_0_6_15-->4_2_8_6
4_2_8_6-->5_0_6_3
5_0_6_3-->6_4_8_16
6_4_8_16-->5_0_6_3
5_0_6_3-->6_4_8_11
6_4_8_11-->5_0_6_3
5_0_6_3-->6_4_8_2
6_4_8_2-->5_0_6_3
5_0_6_3-->6_4_8_13
6_4_8_13-->5_0_6_3
5_0_6_3-->6_4_8_15
6_4_8_15-->5_0_6_3
5_0_6_3-->6_4_8_96
6_4_8_96-->5_0_6_3
5_0_6_3-->6_4_8_7
6_4_8_7-->5_0_6_3
5_0_6_3-->6_4_8_8
6_4_8_8-->5_0_6_3
5_0_6_3-->6_4_8_6
6_4_8_6-->7_0_2_16
7_0_2_16-->8_0_4_11
8_0_4_11-->7_0_2_16
7_0_2_16-->8_0_4_2
8_0_4_2-->7_0_2_16
7_0_2_16-->8_0_4_13
8_0_4_13-->9_4_2_11
9_4_2_11-->8_0_4_13
8_0_4_13-->9_4_2_2
9_4_2_2-->8_0_4_13
8_0_4_13-->9_4_2_15
9_4_2_15-->8_0_4_13
8_0_4_13-->9_4_2_96
9_4_2_96-->8_0_4_13
8_0_4_13-->9_4_2_7
9_4_2_7-->8_0_4_13
8_0_4_13-->9_4_2_8
9_4_2_8-->10_4_4_11
10_4_4_11-->9_4_2_8
9_4_2_8-->10_4_4_2
10_4_4_2-->9_4_2_8
9_4_2_8-->10_4_4_15
10_4_4_15-->9_4_2_8
9_4_2_8-->10_4_4_96
10_4_4_96-->9_4_2_8
9_4_2_8-->10_4_4_7
10_4_4_7-->9_4_2_8
9_4_2_8-->10_4_4_16
10_4_4_16-->9_4_2_8
9_4_2_8-->10_4_4_23
10_4_4_23-->9_4_2_8
9_4_2_8-->10_4_4_39
10_4_4_39-->9_4_2_8
9_4_2_8-->10_4_4_22
10_4_4_22-->9_4_2_8
9_4_2_8-->10_4_4_3
10_4_4_3-->9_4_2_8
9_4_2_8-->8_0_4_13
8_0_4_13-->9_4_2_16
9_4_2_16-->8_0_4_13
8_0_4_13-->9_4_2_23
9_4_2_23-->8_0_4_13
8_0_4_13-->9_4_2_39
9_4_2_39-->8_0_4_13
8_0_4_13-->9_4_2_22
9_4_2_22-->8_0_4_13
8_0_4_13-->9_4_2_3
9_4_2_3-->8_0_4_13
8_0_4_13-->7_0_2_16
7_0_2_16-->8_0_4_15
8_0_4_15-->7_0_2_16
7_0_2_16-->8_0_4_96
8_0_4_96-->7_0_2_16
7_0_2_16-->8_0_4_7
8_0_4_7-->7_0_2_16
7_0_2_16-->8_0_4_8
8_0_4_8-->7_0_2_16
7_0_2_16-->8_0_4_16
8_0_4_16-->7_0_2_16
7_0_2_16-->8_0_4_23
8_0_4_23-->7_0_2_16
7_0_2_16-->8_0_4_39
8_0_4_39-->7_0_2_16
7_0_2_16-->8_0_4_22
8_0_4_22-->7_0_2_16
7_0_2_16-->8_0_4_3
8_0_4_3-->7_0_2_16
7_0_2_16-->6_4_8_6
6_4_8_6-->7_0_2_11
7_0_2_11-->8_0_4_16
8_0_4_16-->7_0_2_11
7_0_2_11-->8_0_4_2
8_0_4_2-->7_0_2_11
7_0_2_11-->8_0_4_13
8_0_4_13-->7_0_2_11
7_0_2_11-->8_0_4_15
8_0_4_15-->7_0_2_11
7_0_2_11-->8_0_4_96
8_0_4_96-->7_0_2_11
7_0_2_11-->8_0_4_7
8_0_4_7-->7_0_2_11
7_0_2_11-->8_0_4_8
8_0_4_8-->9_4_2_16
9_4_2_16-->8_0_4_8
8_0_4_8-->9_4_2_2
9_4_2_2-->8_0_4_8
8_0_4_8-->9_4_2_13
9_4_2_13-->8_0_4_8
8_0_4_8-->9_4_2_15
9_4_2_15-->8_0_4_8
8_0_4_8-->9_4_2_96
9_4_2_96-->8_0_4_8
8_0_4_8-->9_4_2_7
9_4_2_7-->8_0_4_8
8_0_4_8-->9_4_2_23
9_4_2_23-->8_0_4_8
8_0_4_8-->9_4_2_39
9_4_2_39-->8_0_4_8
8_0_4_8-->9_4_2_22
9_4_2_22-->8_0_4_8
8_0_4_8-->9_4_2_3
9_4_2_3-->10_4_4_16
10_4_4_16-->9_4_2_3
9_4_2_3-->10_4_4_2
10_4_4_2-->11_6_6_16
11_6_6_16-->12_6_10_13
12_6_10_13-->11_6_6_16
11_6_6_16-->12_6_10_15
12_6_10_15-->13_10_4_13
13_10_4_13-->14_10_2_96
14_10_2_96-->13_10_4_13
13_10_4_13-->14_10_2_7
14_10_2_7-->13_10_4_13
13_10_4_13-->14_10_2_16
14_10_2_16-->13_10_4_13
13_10_4_13-->14_10_2_23
14_10_2_23-->13_10_4_13
13_10_4_13-->14_10_2_39
14_10_2_39-->13_10_4_13
13_10_4_13-->14_10_2_22
14_10_2_22-->13_10_4_13
13_10_4_13-->12_6_10_15
12_6_10_15-->13_10_4_96
13_10_4_96-->14_10_2_13
14_10_2_13-->13_10_4_96
13_10_4_96-->14_10_2_7
14_10_2_7-->13_10_4_96
13_10_4_96-->14_10_2_16
14_10_2_16-->13_10_4_96
13_10_4_96-->14_10_2_23
14_10_2_23-->13_10_4_96
13_10_4_96-->14_10_2_39
14_10_2_39-->13_10_4_96
13_10_4_96-->14_10_2_22
14_10_2_22-->15_8_2_13
15_8_2_13-->14_10_2_22
14_10_2_22-->15_8_2_7
15_8_2_7-->14_10_2_22
14_10_2_22-->15_8_2_16
15_8_2_16-->14_10_2_22
14_10_2_22-->15_8_2_23
15_8_2_23-->14_10_2_22
14_10_2_22-->15_8_2_39
15_8_2_39-->14_10_2_22
14_10_2_22-->13_10_4_96
13_10_4_96-->12_6_10_15
12_6_10_15-->13_10_4_7
13_10_4_7-->14_10_2_13
14_10_2_13-->13_10_4_7
13_10_4_7-->14_10_2_96
14_10_2_96-->13_10_4_7
13_10_4_7-->14_10_2_16
14_10_2_16-->13_10_4_7
13_10_4_7-->14_10_2_23
14_10_2_23-->13_10_4_7
13_10_4_7-->14_10_2_39
14_10_2_39-->13_10_4_7
13_10_4_7-->14_10_2_22
14_10_2_22-->13_10_4_7
13_10_4_7-->12_6_10_15
12_6_10_15-->13_10_4_16
13_10_4_16-->14_10_2_13
14_10_2_13-->13_10_4_16
13_10_4_16-->14_10_2_96
14_10_2_96-->13_10_4_16
13_10_4_16-->14_10_2_7
14_10_2_7-->13_10_4_16
13_10_4_16-->14_10_2_23
14_10_2_23-->13_10_4_16
13_10_4_16-->14_10_2_39
14_10_2_39-->13_10_4_16
13_10_4_16-->14_10_2_22
14_10_2_22-->13_10_4_16
13_10_4_16-->12_6_10_15
12_6_10_15-->13_10_4_23
13_10_4_23-->14_10_2_13
14_10_2_13-->13_10_4_23
13_10_4_23-->14_10_2_96
14_10_2_96-->13_10_4_23
13_10_4_23-->14_10_2_7
14_10_2_7-->13_10_4_23
13_10_4_23-->14_10_2_16
14_10_2_16-->13_10_4_23
13_10_4_23-->14_10_2_39
14_10_2_39-->13_10_4_23
13_10_4_23-->14_10_2_22
14_10_2_22-->13_10_4_23
13_10_4_23-->12_6_10_15
12_6_10_15-->13_10_4_39
13_10_4_39-->14_10_2_13
14_10_2_13-->13_10_4_39
13_10_4_39-->14_10_2_96
14_10_2_96-->13_10_4_39
13_10_4_39-->14_10_2_7
14_10_2_7-->13_10_4_39
13_10_4_39-->14_10_2_16
14_10_2_16-->13_10_4_39
13_10_4_39-->14_10_2_23
14_10_2_23-->13_10_4_39
13_10_4_39-->14_10_2_22
14_10_2_22-->13_10_4_39
13_10_4_39-->12_6_10_15
12_6_10_15-->13_10_4_22
13_10_4_22-->14_10_2_13
14_10_2_13-->13_10_4_22
13_10_4_22-->14_10_2_96
14_10_2_96-->15_8_2_13
15_8_2_13-->14_10_2_96
14_10_2_96-->15_8_2_7
15_8_2_7-->14_10_2_96
14_10_2_96-->15_8_2_16
15_8_2_16-->16_8_4_13
16_8_4_13-->15_8_2_16
15_8_2_16-->16_8_4_7
16_8_4_7-->17_8_6_13
17_8_6_13-->16_8_4_7
16_8_4_7-->17_8_6_23
17_8_6_23-->18_10_6_13
18_10_6_13-->17_8_6_23
17_8_6_23-->18_10_6_39
18_10_6_39-->19_10_8_13-->Done

```