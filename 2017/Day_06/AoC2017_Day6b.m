function nsteps = AoC2017_Day6b(banklist)
% Out of curiosity, the debugger would also like to know the size of the loop: starting from a state
% that has already been seen, how many block redistribution cycles must be performed before that
% same state is seen again?
%
% In the example above, 2 4 1 2 is seen again after four cycles, and so the answer in that example
% would be 4.
%
% How many cycles are in the infinite loop that arises from the configuration in your puzzle input?

nbanks = numel(banklist);

memmemo = NaN(size(banklist));
nsteps = 0;
while isempty(intersect(memmemo, banklist, 'rows'))
    memmemo = [memmemo; banklist];
    [maxmem, maxidx] = max(banklist);

    banklist(maxidx) = 0;
    idxlist = mod([maxidx:maxidx+maxmem-1], nbanks)+1;
    summer = histcounts(idxlist, 1:nbanks+1);
    banklist = banklist + summer;

    nsteps = nsteps + 1;
end
end
