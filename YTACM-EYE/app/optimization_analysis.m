# Optimization analysis

#nCombinations
# most unknowns first, unsorted, fewest unknowns first
expert=[2894674 864 179]
difficult=[14698240	468	237]
medium=[3933	468	48]
easy=[49	44	25]

subplot(1,2,1)
plot([easy;medium;difficult;expert]');
title('number of visits based on sorting algorithm')
legend(['easy'; 'medium'; 'difficult'; 'expert']);
set(gca, 'XTick', 1:3, 'XTickLabel', {'most unknowns first'; 'no sorting'; 'fewest unknowns first'});

subplot(1,2,2)
semilogy([easy;medium;difficult;expert]');
title('number of visits based on sorting algorithm')
legend(['easy'; 'medium'; 'difficult'; 'expert']);
set(gca, 'XTick', 1:3, 'XTickLabel', {'most unknowns first'; 'no sorting'; 'fewest unknowns first'});
