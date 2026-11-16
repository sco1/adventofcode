package main

import (
	"fmt"

	"github.com/sco1/adventofcode/internal/aoc"
)

func main() {
	puzzleInput := aoc.ReadInput()
	fmt.Printf("Part One: %v\n", santaElevator(puzzleInput, 1))
	fmt.Printf("Part Two: %v\n", santaElevator(puzzleInput, 2))
}

func santaElevator(directions string, part int) int {
	var level int
	for i, d := range directions {
		switch d {
		case '(':
			level++
		case ')':
			level--
		default:
			panic(fmt.Sprintf("Unknown instruction at idx %v: %v", i, d))
		}

		if part == 2 && level == -1 {
			return i + 1
		}
	}

	return level
}
