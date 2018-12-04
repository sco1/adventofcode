function output = AoC2017_Day4b(filepath)
% For added security, yet another system policy has been put in place. Now,
% a valid passphrase must contain no two words that are anagrams of each 
% other - that is, a passphrase is invalid if any word's letters can be 
% rearranged to form any other word in the passphrase.
% 
% For example:
% 
% abcde fghij is a valid passphrase.
% abcde xyz ecdab is not valid - the letters from the third word can be 
%                 rearranged to form the first word.
% a ab abc abd abf abj is a valid passphrase, because all letters need to 
%                      be used when forming another word.
% iiii oiii ooii oooi oooo is valid.
% oiii ioii iioi iiio is not valid - any of these words can be rearranged 
%                     to form any other word.
%
% Under this new system policy, how many passphrases are valid?
passlist = importdata(filepath);

test = false(size(passlist));
for ii = 1:numel(passlist)
    passlist{ii} = string(strsplit(passlist{ii}));
    for jj = 1:numel(passlist{ii})
        % WHY THE FUCK CAN'T MATLAB NATIVELY SORT STRINGS?
        % Look at this monstrosity...
        passlist{ii}(jj) = string(sort(char(passlist{ii}(jj))));
    end
    [~, ~, tmp] = unique(passlist{ii});
    test(ii) = any(accumarray(tmp, 1) > 1);
end

output = sum(~test);
end