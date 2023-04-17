package main

import (
	"fmt"
	"os"
	"strings"
)

var puzzleInputFile = "./puzzle_input.txt"

func main() {
	puzzleInput := readPuzzleInput(puzzleInputFile)
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

func readPuzzleInput(filename string) string {
	rawInput, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	return strings.TrimSpace(string(rawInput))
}
