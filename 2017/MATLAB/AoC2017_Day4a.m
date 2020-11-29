function output = AoC2017_Day4a(filepath)
% A new system policy has been put in place that requires all accounts to 
% use a passphrase instead of simply a password. A passphrase consists of a
% series of words (lowercase letters) separated by spaces.
% 
% To ensure security, a valid passphrase must contain no duplicate words.
% 
% For example:
% 
% aa bb cc dd ee is valid.
% aa bb cc dd aa is not valid - the word aa appears more than once.
% aa bb cc dd aaa is valid - aa and aaa count as different words.
%
% The system's full passphrase list is available as your puzzle input. How many passphrases are valid?
passlist = importdata(filepath);

test = false(size(passlist));
for ii = 1:numel(passlist)
    passlist{ii} = string(strsplit(passlist{ii}));
    [~, ~, tmp] = unique(passlist{ii});
    test(ii) = any(accumarray(tmp, 1) > 1);
end

output = sum(~test);
end
