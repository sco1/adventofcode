function aoc_2019_day1()
input_data = readmatrix("./puzzle_input.txt", "NumHeaderLines", 0);

% Part 1
disp(sum(calculate_propellant(input_data)))

% Part 2
disp(sum(calculate_stage_propellant(input_data)))
end


function [output] = calculate_propellant(mass)
output = floor(mass ./ 3) - 2;
end


function [output] = calculate_stage_propellant(mass)
output = zeros(size(mass));

for i = 1:numel(mass)
    fuel_step = calculate_propellant(mass(i));
    while fuel_step > 0
        output(i) = output(i) + fuel_step;
        fuel_step = calculate_propellant(fuel_step);
    end
end
end