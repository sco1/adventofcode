calorie_counts = parse_calories('./puzzle_input.txt');
% calorie_counts = parse_calories('./sample_input.txt');

fprintf('Part One: %u\n', densest_elf(calorie_counts));
fprintf('Part Two: %u\n', densest_trio(calorie_counts));


function [calorie_counts] = parse_calories(filepath)
% Parse the provided snack list and calculate the number of calories carried by each elf.
%
% Elves are assumed to be delimited by a blank line.
    arguments
        filepath char {mustBeFile}
    end

    calorie_counts = [];
    calorie_sum = 0;
    fid = fopen(filepath, 'r');
    while ~feof(fid)
        line = fgetl(fid);
        if numel(line) == 0
            calorie_counts(end+1) = calorie_sum;  %#ok<AGROW>
            calorie_sum = 0;
            continue
        end

        calorie_sum = calorie_sum + str2double(line);
    end
    fclose(fid);

    % Catch any trailing calories from the last elf
    if calorie_counts > 0
        calorie_counts(end+1) = calorie_sum;
    end
end


function [calories] = densest_elf(calorie_counts)
    % Identify the number of calories carried by the elf with the most snack calories.
    arguments
        calorie_counts (:, 1) {mustBeNumeric, mustBeNonempty, mustBeVector}
    end

    calories = max(calorie_counts);
end


function [calories] = densest_trio(calorie_counts)
    % Calculate the total calories carried by the three densest elves.
    arguments
        calorie_counts (:, 1) {mustBeNumeric, mustBeNonempty, mustBeVector}
    end

    calorie_counts = sort(calorie_counts);
    calories = sum(calorie_counts(end-2:end));
end
