package main

import (
	_ "embed"
	"strings"
)

//go:embed input.txt
var input string

func SolveEmbed() (int, int) {
	arr_bags := strings.Split(strings.TrimSuffix(input, "\n"), "\n")
	var bags [300]string
	copy(bags[:], arr_bags)

	// Part 1
	totalPriorities := 0

	for z := 0; z < len(bags); z++ {
		bag := bags[z]
		var duplicatedItem byte
		n := len(bag)

	out:
		for i := 0; i < n/2; i++ {
			for j := n / 2; j < n; j++ {
				if bag[i] == bag[j] {
					duplicatedItem = bag[i]
					break out
				}
			}
		}

		if duplicatedItem >= 'a' {
			totalPriorities += int(duplicatedItem) - 96
		} else {
			totalPriorities += int(duplicatedItem) - 38
		}
	}

	// Part 2
	totalBadgePriorities := 0

	for bagIndex := 0; bagIndex < len(bags); bagIndex += 3 {
		var duplicatedItem byte

	out_3:
		for i := 0; i < len(bags[bagIndex]); i++ {
			for j := 0; j < len(bags[bagIndex+1]); j++ {
				if bags[bagIndex+1][j] == bags[bagIndex][i] {
					continue
				}
				for k := 0; k < len(bags[bagIndex+2]); k++ {
					if bags[bagIndex+2][k] == bags[bagIndex][i] {
						duplicatedItem = bags[bagIndex][i]
						break out_3
					}
				}
			}
		}

		if duplicatedItem >= 'a' {
			totalBadgePriorities += int(duplicatedItem) - 96
		} else {
			totalBadgePriorities += int(duplicatedItem) - 38
		}
	}

	return totalPriorities, totalBadgePriorities
}
