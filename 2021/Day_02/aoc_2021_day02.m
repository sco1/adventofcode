instructions = parse_commands('./puzzle_input.txt');
% commands = parse_commands('./sample_input.txt');

fprintf('Part One: %u\n', run_basic_sub(commands));
fprintf('Part Two: %u\n', run_aiming_sub(commands));


function [instructions] = parse_commands(filepath)
% Parse the provided depth soundings into an n x 1 vector.
arguments
    filepath char {mustBeFile}
end

instructions = readtable(filepath, TextType="string");
instructions.Properties.VariableNames = {'instruction', 'magnitude'};
end

function [final_position] = run_basic_sub(commands)
% Interpret command instructions per the YOLO submarine manual-less instructions.
%
% Instructions are interpreted as written.
arguments
    commands table {mustBeNonempty}
end

depth = 0;
horizontal = 0;

n_steps = size(commands, 1);
for ii = 1:n_steps
    magnitude = commands.magnitude(ii);
    switch commands.instruction(ii)
        case "forward"
            horizontal = horizontal + magnitude;
        case "up"
            depth = depth - magnitude;
        case "down"
            depth = depth + magnitude;
        otherwise
            error("Unknown instruction '%s'", commands.instruction(ii))
    end
end

final_position = depth * horizontal;
end

function [final_position] = run_aiming_sub(commands)
% Interpret command instructions per the more complicated submarine manual.
%
% The "up" and "down" instructions change the submarine's aim, and the "forward" instruction
% modifies both the horizontal position and depth of the submarine.
arguments
    commands table {mustBeNonempty}
end

aim = 0;
depth = 0;
horizontal = 0;

n_steps = size(commands, 1);
for ii = 1:n_steps
    magnitude = commands.magnitude(ii);
    switch commands.instruction(ii)
        case "forward"
            horizontal = horizontal + magnitude;
            depth = depth + aim*magnitude;
        case "up"
            aim = aim - magnitude;
        case "down"
            aim = aim + magnitude;
        otherwise
            error("Unknown instruction '%s'", commands.instruction(ii))
    end
end

final_position = depth * horizontal;
end
