function output = AoC2017_Day2b(filepath)
% It sounds like the goal is to find the only two numbers in each row where 
% one evenly divides the other - that is, where the result of the division 
% operation is a whole number. They would like you to find those numbers on 
% each line, divide them, and add up each line's result.
% 
% For example, given the following spreadsheet:
% 
% 5 9 2 8
% 9 4 7 3
% 3 8 6 5
% 
% In the first row, the only two numbers that evenly divide are 8 and 2; 
% the result of this division is 4.
% In the second row, the two numbers are 9 and 3; the result is 3.
% In the third row, the result is 2.
% 
% In this example, the sum of the results would be 4 + 3 + 2 = 9.

m = importdata(filepath);
nrows = size(m, 1);

output = 0;
for ii = 1:nrows
    pairs = sort(nchoosek(m(ii,:), 2), 2, 'descend');
    test = mod(pairs(:, 1), pairs(:, 2));
    pairidx = find(test == 0, 1);
    
    output = output + pairs(pairidx, 1)/pairs(pairidx, 2);
end

end