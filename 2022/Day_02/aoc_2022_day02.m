game_rounds = parse_guide('./puzzle_input.txt');
% game_rounds = parse_guide('./sample_input.txt');

% Map shape combinations to game point outcome, then add in the per-shape score. Keep as separate
% variables to help with Part 2's outcome lookup
outcome_board = [
%   A  B  C
    3, 0, 6;  % X
    6, 3, 0;  % Y
    0, 6, 3;  % Z
];
score_board = outcome_board + [1; 2; 3];

fprintf('Part One: %u\n', play_game(game_rounds, score_board));
fprintf('Part Two: %u\n', play_perfect_game(game_rounds, outcome_board, score_board));


function [round_guide] = parse_guide(filepath)
    % Parse the provided strategy guide into a table of its components.
    %
    % Columns are added mapping the guide's symbols (ABC & XYZ) to indices corresponding to the
    % generated outcome board. i.e. A == X == 1, B == Y == 2, and C == Z == 3.
    arguments
        filepath char {mustBeFile}
    end

    round_guide = readtable(filepath, "ReadVariableNames", false, "TextType", "string");
    round_guide.Properties.VariableNames = ["l", "r"];
    round_guide.norm_l = double(char(round_guide.l)) - double('A') + 1;
    round_guide.norm_r = double(char(round_guide.r)) - double('Z') + 3;
end


function [final_score] = play_game(round_guide, score_board)
    % Calculate the total game score where each line of the guide is the shape to play.
    arguments
        round_guide (:, 4) table {mustBeNonempty}
        score_board (3, 3) {mustBeNumeric}
    end

    % Our scoreboard matrix is really just a lookup table, so we can index into it with the shapes
    % that we mapped during parsing.
    idx = sub2ind(size(score_board), round_guide.norm_r, round_guide.norm_l);
    final_score = sum(score_board(idx));
end

function [final_score] = play_perfect_game(round_guide, outcome_board, score_board)
    % Calculate the total game score where each line of the guide is the round outcome.
    arguments
        round_guide (:, 4) table {mustBeNonempty}
        outcome_board (3, 3) {mustBeNumeric}
        score_board (3, 3) {mustBeNumeric}
    end

    target_score = [0, 3, 6];  % Maps to [X, Y, Z]
    n_rounds = size(round_guide, 1);
    idx = zeros(n_rounds, 1);
    for ii = 1:n_rounds
        % For each round, look up the shape we need to play to achieve the target outcome (score)
        % Then transform this index so we can use it with the scoreboard
        row_idx = find( ...
            outcome_board(:, round_guide.norm_l(ii)) == target_score(round_guide.norm_r(ii)), 1 ...
        );
        idx(ii) = sub2ind(size(outcome_board), row_idx, round_guide.norm_l(ii));
    end

    final_score = sum(score_board(idx));
end
