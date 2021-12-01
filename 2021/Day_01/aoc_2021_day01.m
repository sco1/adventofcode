soundings = parse_soundings('./puzzle_input.txt');
% soundings = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263];

fprintf('Part One: %u\n', count_adjacent(soundings));
fprintf('Part Two: %u\n', count_sums(soundings, 3));


function [soundings] = parse_soundings(filepath)
% Parse the provided depth soundings into an n x 1 vector.
arguments
    filepath char {mustBeFile}
end

fid = fopen(filepath, 'r');
soundings = fscanf(fid, '%u');
fclose(fid);
end

function [n_ascending] = count_adjacent(soundings)
% Count the number of times the depth sounding increases from the previous measurement.
arguments
    soundings (:, 1) {mustBeNumeric, mustBeNonempty, mustBeVector}
end

n_ascending = sum(diff(soundings) > 0);
end

function [n_ascending] = count_sums(soundings, width)
% Count the number of times the sum of a sliding window increases from the previous window's sum.
arguments
    soundings (:, 1) {mustBeNumeric, mustBeNonempty, mustBeVector}
    width (1, 1) {mustBeInteger} = 3
end

n_windows = length(soundings) - width + 1;
windows = zeros(n_windows, 1);
for ii = 1:n_windows
    windows(ii) = sum(soundings(ii:(ii+width-1)));
end

n_ascending = sum(diff(windows) > 0);
end
