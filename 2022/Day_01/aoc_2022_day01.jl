using Printf

function parse_input(filepath::String)
    calorie_counts = Array{Int, 1}()
    calories = 0
    for line in eachline(filepath)
        if length(line) == 0
            push!(calorie_counts, calories)
            calories = 0
            continue
        end

        calories += parse(Int, line)
    end

    if calories > 0
        push!(calorie_counts, calories)
    end

    return sort(calorie_counts, rev=true)
end

counts = parse_input("./puzzle_input.txt")
@printf("Part 1: %i\n", counts[1])
@printf("Part2: %i\n", sum(counts[1:3]))
