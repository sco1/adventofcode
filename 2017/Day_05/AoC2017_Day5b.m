function nsteps = AoC2017_Day5b(filepath)
% Now, the jumps are even stranger: after each jump, if the offset was three or more, instead
% decrease it by 1. Otherwise, increase it by 1 as before.
%
% Using this rule with the above example, the process now takes 10 steps, and the offset values
% after finding the exit are left as 2 3 2 3 -1.
%
% How many steps does it now take to reach the exit?
steps = importdata(filepath);

pos = 1;
nsteps = 0;
while pos <= numel(steps)
    currentpos = pos;
    pos = pos + steps(pos);

    if steps(currentpos) >= 3
        steps(currentpos) = steps(currentpos) - 1;
    else
        steps(currentpos) = steps(currentpos) + 1;
    end
    nsteps = nsteps + 1;
end
end
