package main

import (
	_ "embed"
)

//go:embed input.txt
var input string

func FindMarker(data string, windowSize int) int {
	index := -2
	var flags ['z' + 1]byte

	for i := 0; i < windowSize; i++ {
		flags[data[i]] += 1
	}

	for i := windowSize; i < len(data); i++ {
		flags[data[i]] += 1

		found := true
		for j := 0; found && j < windowSize; j++ {
			found = found && (flags[data[i-j]] == 1)
		}
		if found {
			index = i
			break
		}
		flags[data[i-windowSize]] -= 1
	}
	return index + 1
}

func Solve() (int, int) {
	return FindMarker(input, 4-1), FindMarker(input, 14-1)
}
