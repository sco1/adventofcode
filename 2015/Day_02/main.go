package main

import (
	"fmt"
	"os"
	"strings"
)

var puzzleInputFile = "./puzzle_input.txt"

func main() {
	puzzleInput := readPuzzleInput(puzzleInputFile)

	paper, ribbon := wrapPresents(puzzleInput)
	fmt.Printf("Part One: %v\n", paper)
	fmt.Printf("Part Two: %v\n", ribbon)
}

func readPuzzleInput(filename string) string {
	rawInput, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	return strings.TrimSpace(string(rawInput))
}

func wrapPresents(dimensions string) (int, int) {
	var totalArea, totalRibbon int

	for _, present := range strings.Split(dimensions, "\n") {
		var length, width, height int
		_, err := fmt.Sscanf(present, "%dx%dx%d", &length, &width, &height)
		if err != nil {
			panic(err)
		}

		totalArea += calcPaper(length, width, height)
		totalRibbon += calcRibbon(length, width, height)
	}

	return totalArea, totalRibbon
}

func calcPaper(length int, width int, height int) int {
	var totalArea int

	totalArea += 2*(length*width) + 2*(width*height) + 2*(height*length)
	totalArea += minVal((length * width), (width * height), (height * length)) // Paper slack

	return totalArea
}

func calcRibbon(length int, width int, height int) int {
	var totalLength int

	totalLength += minVal(2*(length+width), 2*(length+height), 2*(width+height))
	totalLength += length * width * height // Bow

	return totalLength
}

func minVal(values ...int) int {
	minArea := values[0]
	for _, a := range values {
		if a < minArea {
			minArea = a
		}
	}

	return minArea
}
