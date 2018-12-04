function output = AoC2017_Day1a(str)
% Input a string of digits
% 
% Review a sequence of digits and find the sum of all digits that match the
% next digit in the list. The list is circular, so the digit after the last
% digit is the first digit in the list.
%
% e.g.
% 1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the 
%      second digit and the third digit (2) matches the fourth digit
% 1111 produces 4 because each digit (all 1) matches the next
% 1234 produces 0 because no digit matches the next
% 91212129 produces 9 because the only digit that matches the next one is 
%          the last digit, 9

% Split digits into integer array, use uin8 since our range is [0, 9]
% Intermediate double because MATLAB has no string -> integer function
m = uint8(double(regexp(str, '\d', 'match')));

% Loop over elements, add them to the sum if their right-hand neighbor is
% the same
output = 0;
for ii = 1:(length(m) - 1)
    if m(ii) == m(ii + 1)
        output = output + double(m(ii));
    end
end

% Check if first & last are the same and add to sum if they are (list is
% circular)

if m(1) == m(end)
    output = output + double(m(1));
end
end