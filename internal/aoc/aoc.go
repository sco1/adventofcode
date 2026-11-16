// Package aoc holds helpers shared by the Go puzzle solutions.
package aoc

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

// ReadInput returns the whitespace-trimmed contents of the calling solution's puzzle input.
//
// Solutions live in a `Day_NN/go/` folder, and the puzzle input is `Day_NN/puzzle_input.txt`, so
// the file is located relative to the caller's source file rather than the working directory.
func ReadInput() string {
	_, callerFile, _, ok := runtime.Caller(1)
	if !ok {
		panic("could not determine the calling source file")
	}

	inputPath := filepath.Join(filepath.Dir(callerFile), "..", "puzzle_input.txt")
	rawInput, err := os.ReadFile(inputPath)
	if err != nil {
		panic(err)
	}

	return strings.TrimSpace(string(rawInput))
}
