rucksacks = parse_puzzle_input('./puzzle_input.txt');
% rucksacks = parse_puzzle_input('./sample_input.txt');

fprintf('Part One: %u\n', score_rucksacks(rucksacks));
fprintf('Part Two: %u\n', score_grouped(rucksacks));


function [rucksacks] = parse_puzzle_input(filepath)
    % Load rucksack descriptions from the provided file, assumed to be one rucksack per line.
    arguments
        filepath char {mustBeFile}
    end

    rucksacks = string(fileread(filepath)).strip().splitlines();
end


function [score] = score_letter(letter)
    % Calculate the item priority.
    %
    % Priority is assigned as follows:
    %     * Lowercase item types 'a' through 'z' have priorities 1 through 26
    %     * Uppercase item types 'A' through 'Z' have priorities 27 through 52
    arguments
        letter (1, 1) {mustBeA(letter, "char"), mustBeNonempty}
    end

    if isstrprop(letter, "lower")
        score = double(letter) - double('a') + 1;
    else
        score = double(letter) - double('A') + 27;
    end
end


function [overlap_priority] = calculate_overlap_priority(rucksack)
    % Calculate the priority of the overlapping item in the provided rucksack's compartments.
    %
    % The following assumptions are made:
    %     * Items are identified by single ASCII letters, where capital and lowercase are distinct
    %     * The rucksack can be evenly divisible into 2 compartments
    %     * There is only one overlapping item per rucksack
    arguments
        rucksack (1, 1) {mustBeA(rucksack, "string"), mustBeNonempty}
    end

    width = strlength(rucksack) / 2;
    left = rucksack.extractBefore(width + 1);
    right = rucksack.extractAfter(width);

    common = intersect(left{1}, right{1});
    overlap_priority = score_letter(common);
end


function [total_priority] = score_rucksacks(rucksacks)
    % Calculate the total priority score for the provided rucksacks.
    arguments
        rucksacks (:, 1) {mustBeA(rucksacks, "string"), mustBeNonempty}
    end

    total_priority = sum(arrayfun(@calculate_overlap_priority, rucksacks));
end


function [total_priority] = score_grouped(rucksacks)
    % Calculate the total rucksack priority score for each group of 3 elves.
    %
    % The following assumptions are made:
    %     * Items are identified by single ASCII letters, where capital and lowercase are distinct
    %     * The elves can be evenly grouped into groups of 3
    %     * There is only one overlapping item per group
    arguments
        rucksacks (:, 1) {mustBeA(rucksacks, "string"), mustBeNonempty}
    end

    group_size = 3;
    total_priority = 0;
    for ii = 1:group_size:numel(rucksacks)
        group = rucksacks(ii:(ii + group_size - 1));
        common = intersect(intersect(group{1}, group{2}), group{3});
        total_priority = total_priority + score_letter(common);
    end
end
