puzzle_input = read_puzzle_input("./puzzle_input.txt");

test_part_1
fprintf("Part 1: %d\n", part_1(puzzle_input))

test_part_2
fprintf("Part 2: %d\n", part_2(puzzle_input))


function puzzle_input = read_puzzle_input(puzzle_input_path)
    arguments
        puzzle_input_path (1,1) string {mustBeFile}
    end

    puzzle_input = readlines(puzzle_input_path, "EmptyLineRule", "skip");
end


function floor = part_1(instructions)
    arguments
        instructions (1, 1) string
    end

    floor = 0;
    for ii = 1:strlength(instructions)
        switch instructions{1}(ii)
            case "("
                floor = floor + 1;
            case ")"
                floor = floor - 1;
        end
    end
end


function test_part_1()
    test_cases = dictionary( ...
        ["(())", "()()", "(((", "(()(()(", "))(((((", "())", "))(", ")))", ")())())"], ...
        [0, 0, 3, 3, 3, -1, -1, -3, -3] ...
    );

    for ii = 1:numel(test_cases.keys)
        instruction_case = test_cases.keys{ii};
        assert(part_1(instruction_case)==test_cases(instruction_case))
    end
end


function basement_instruction = part_2(instructions)
    arguments
        instructions (1, 1) string
    end

    floor = 0;
    for ii = 1:strlength(instructions)
        switch instructions{1}(ii)
            case "("
                floor = floor + 1;
            case ")"
                floor = floor - 1;
        end

        if floor == -1
            basement_instruction = ii;
            return
        end
    end
end

function test_part_2()
    test_cases = dictionary( ...
        [")", "()())"], ...
        [1, 5] ...
    );

    for ii = 1:numel(test_cases.keys)
        instruction_case = test_cases.keys{ii};
        assert(part_2(instruction_case)==test_cases(instruction_case))
    end
end
