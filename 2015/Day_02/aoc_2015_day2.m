puzzle_input = read_puzzle_input("./puzzle_input.txt");

test_part_1
fprintf("Part 1: %d\n", part_1(puzzle_input))

test_part_2
fprintf("Part 2: %d\n", part_2(puzzle_input))


function puzzle_input = read_puzzle_input(puzzle_input_path)
    arguments
        puzzle_input_path (1,1) string {mustBeFile}
    end

    fid = fopen(puzzle_input_path);
    raw_lines = textscan(fid, "%ux%ux%u", "CollectOutput", true);
    fclose(fid);

    puzzle_input = raw_lines{1};
end


function paper_footage = part_1(present_dimensions)
    arguments
        present_dimensions (:, 3)
    end

    side_areas = [
        present_dimensions(:, 1).*present_dimensions(:, 2), ...
        present_dimensions(:, 1).*present_dimensions(:, 3), ...
        present_dimensions(:, 2).*present_dimensions(:, 3), ...
    ];
    side_areas = sort(side_areas, 2);
    smallest_side = side_areas(:, 1);

    paper_footage = sum(sum(2*side_areas, 2, "native") + smallest_side);
end


function test_part_1()
    test_cases = {
        [2, 3, 4], 58;
        [1, 1, 10], 43;
    };

    n_tests = size(test_cases, 1);
    for ii = 1:n_tests
        dims = test_cases{ii, 1};
        truth_value = test_cases{ii, 2};

        assert(part_1(dims) == truth_value);
    end
end


function total_ribbon = part_2(present_dimensions)
    arguments
        present_dimensions (:, 3)
    end

    side_perimeters = [
        2*(present_dimensions(:, 1)+present_dimensions(:, 2)), ...
        2*(present_dimensions(:, 1)+present_dimensions(:, 3)), ...
        2*(present_dimensions(:, 2)+present_dimensions(:, 3)), ...
    ];
    side_perimeters = sort(side_perimeters, 2);

    present_volumes = prod(present_dimensions, 2, "native");
    total_ribbon = sum(side_perimeters(:, 1) + present_volumes);
end

function test_part_2()
    test_cases = {
        [2, 3, 4], 34;
        [1, 1, 10], 14;
    };

    n_tests = size(test_cases, 1);
    for ii = 1:n_tests
        dims = test_cases{ii, 1};
        truth_value = test_cases{ii, 2};

        assert(part_2(dims) == truth_value);
    end
end
