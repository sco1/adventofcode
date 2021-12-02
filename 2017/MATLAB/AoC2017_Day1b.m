function output = AoC2017_Day1b(str)
% Input a string of digits Assume an even number of digits
%
% Consider the digit halfway around the circular list. That is, if your list contains 10 items, only
% include a digit in your sum if the digit 10/2 = 5 steps forward matches it. Fortunately, your list
% has an even number of elements.
%
% For example:
%
%   * 1212 produces 6, the list contains 4 items, and all four digits match the digit 2 items ahead
%   * 1221 produces 0, because every comparison is between a 1 and a 2
%   * 123425 produces 4, because both 2s match each other, but no other digit has a match
%   * 123123 produces 12
%   * 12131415 produces 4

% Split digits into integer array, use uin8 since our range is [0, 9] Intermediate double because
% MATLAB has no string -> integer function
m = uint8(double(regexp(str, '\d', 'match')));

% Loop over all digits, checking ndigits/2 steps forward to see if the digit matches. If it matches,
% add it to the total
output = 0;
ndigits = length(m);
checkstep = ndigits/2;
for ii = 1:ndigits
    % Use modulo to find circular index
    testidx = mod(ii + checkstep, ndigits);
    if testidx == 0
        % Catch case where testidx == length(m), which makes modulo 0
        testidx = ndigits;
    end

    if m(ii) == m(testidx)
        output = output + double(m(ii));
    end
end
