# Optimization analysis

#nCombinations
# worst, bruteforce, best
expert=[5789328 1708 338]
difficult=[3495390 4672 216]
medium=[7850 366 80]
easy=[88 88 40]

subplot(1,2,1)
plot([easy;medium;difficult;expert]');
title('number of visits based on sorting algorithm')
legend(['easy'; 'medium'; 'difficult'; 'expert']);
set(gca, 'XTick', 1:3, 'XTickLabel', {'worst'; 'no sorting'; 'best'});

subplot(1,2,2)
semilogy([easy;medium;difficult;expert]');
title('number of visits based on sorting algorithm')
legend(['easy'; 'medium'; 'difficult'; 'expert']);
set(gca, 'XTick', 1:3, 'XTickLabel', {'worst'; 'no sorting'; 'best'});
