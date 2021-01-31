expense_report = parse_expense_report('./puzzle_input.txt');

target_value = 2020;
fprintf('Part One: %u\n', find_entry_product(expense_report, target_value, 2));
fprintf('Part Two: %u\n', find_entry_product(expense_report, target_value, 3));


function [expense_report] = parse_expense_report(filepath)
% Parse the provided expense report file into an nx1 array of integers
    arguments
        filepath char {mustBeFile}
    end

fid = fopen(filepath, 'r');
expense_report = fscanf(fid, '%lu');  % Use 64-bit to keep values as integers vs. double
fclose(fid);
end


function [result_prod] = find_entry_product(expense_report, target, n_values)
% Iterate over all combinations of N_VALUES expense values from the provided expense report
% until a combination is found that sums to the provided TARGET value, then return the product
% of the value combination.
    arguments
        expense_report (1, :)
        target {mustBePositive}
        n_values {mustBePositive}
    end

check_combinations = nchoosek(expense_report, n_values);
sums = sum(check_combinations, 2);  % Row-wise summation

for ii = 1:length(sums)
    if sums(ii) == target
        break
    end
end
result_prod = prod(check_combinations(ii, :));
end
