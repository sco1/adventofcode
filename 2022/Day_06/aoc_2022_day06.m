data_buffer = parse_buffer('./puzzle_input.txt');
% data_buffer = parse_buffer('./sample_input.txt');

fprintf('Part One: %u\n', locate_start_marker(data_buffer));
fprintf('Part Two: %u\n', locate_start_marker(data_buffer, 14));


function [data_buffer] = parse_buffer(filepath)
    arguments
        filepath char {mustBeFile}
    end

    data_buffer = string(fileread(filepath)).strip();
end


function [start_idx] = locate_start_marker(data_buffer, chunk_width)
    % Identify the 1st position where the chunk_width most recently received characters all differ.
    %
    % Start marker location is indexed as the number of characters from the beginning of the buffer
    % to the end of the first start marker.
    arguments
        data_buffer {mustBeA(data_buffer, "string"), mustBeNonempty}
        chunk_width (1, 1) {mustBeInteger, mustBeNonzero} = 4
    end

    start_idx = -1;  % Sentinel value
    for ii = 1:(strlength(data_buffer) - chunk_width)
        chunk = data_buffer.extractBetween(ii, (ii + chunk_width - 1));
        if strlength(chunk) == strlength(unique(chunk{1}))
            start_idx = (ii + chunk_width - 1);
            break
        end
    end
end
