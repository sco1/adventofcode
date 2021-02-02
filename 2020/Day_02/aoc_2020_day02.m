specs = parse_password_spec('./puzzle_input.txt');

% Validate each spec against the rules for both parts of the puzzle
% Column 1 for Part 1, Column 2 for Part 2
% Set UniformOutput to false because we're not returning a scalar
validate_specs = arrayfun(@is_valid_password, specs, 'UniformOutput', false);
validate_specs = vertcat(validate_specs{:});  % Denest into array
n_valid = sum(validate_specs, 1);
fprintf("Part One: %d valid passwords\n", n_valid(1))
fprintf("Part Two: %d valid passwords\n", n_valid(2))

function [out_specs] = parse_password_spec(filepath)
% Parse the provided puzzle input into its password specifications & test
% passwords.
%
% Puzzle input is assumed to be of the following form:
%     <min occurrences>-<max occurrences> <letter>: <test password>
%
%     e.g. "1-3 a: abcde"
arguments
    filepath char {mustBeFile}
end

raw_lines = splitlines(string(fileread(filepath)));
% Splitlines will keep empty lines, which we might have at the end
if isempty(raw_lines{end})
    raw_lines(end) = [];
end

n_passwords = numel(raw_lines);
out_specs(n_passwords) = struct( ...
    "key_l", [], ...
    "key_r", [], ...
    "key_letter", "", ...
    "password", "" ...
);

exp = "(\d+)-(\d+) ([A-Za-z]): ([A-Za-z]+)";
for ii = 1:n_passwords
    matches = regexp(raw_lines{ii}, exp, "tokens");
    matches = [matches{:}];  % Denest cells since we're going line-by-line
    
    out_specs(ii).key_l = str2double(matches{1});
    out_specs(ii).key_r = str2double(matches{2});
    out_specs(ii).key_letter = string(matches{3});
    out_specs(ii).password = string(matches{4});
end
end


function [is_valid] = is_valid_password(spec)
% Count the number of valid passwords according to the two policy spec
% interpretations:
%     * Spec 0 checks the keys against occurrences of the key letter
%     * Spec 1 checks the index (1-indexed) of the keys in the password for
%       at least one match of the key letter
arguments
    spec (1,:) struct
end

% Check validity for Part 1, where the keys represent the (inclusive) range
% of the number of key letters in the password
n_letter = count(spec.password, spec.key_letter);
is_valid_pt1 = (spec.key_l <= n_letter) & ...
    (n_letter <= spec.key_r);

% Check validity for Part 2, where the keys represent indices to check
% against the key letter; exactly one of these indices must contain the
% key, so we have an XOR
is_valid_pt2 = xor( ...
    spec.password.extract(spec.key_l) == spec.key_letter, ...
    spec.password.extract(spec.key_r) == spec.key_letter ...
);

is_valid = [is_valid_pt1, is_valid_pt2];
end
