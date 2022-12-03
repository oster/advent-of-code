package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func GetItemPriority(item rune) int {
	if item >= 'a' && item <= 'z' {
		return int(item) - int('a') + 1
	} else { // assume item >= 'A' and item <= 'Z'
		return int(item) - int('A') + 26 + 1
	}
}

func main() {
	dataFile, err := os.Open("input.txt")
	if err != nil {
		log.Fatal("failed to open data file")
	}

	var bags []string = make([]string, 0)

	fileScanner := bufio.NewScanner(dataFile)
	for fileScanner.Scan() {
		bags = append(bags, fileScanner.Text())
	}
	dataFile.Close()

	// Part 1
	totalPriorities := 0

	for _, bag := range bags {
		pivot := len(bag) / 2
		firstCompartment, secondComparment := bag[:pivot], bag[pivot:]
		var duplicatedItem rune

	out:
		for _, item := range firstCompartment {
			for _, item2 := range secondComparment {
				if item == item2 {
					duplicatedItem = item
					break out
				}
			}
		}
		totalPriorities += GetItemPriority(duplicatedItem)
	}

	// Part 2
	totalBadgePriorities := 0

	for bagIndex := 0; bagIndex < len(bags); bagIndex += 3 {
		var duplicatedItem rune

	out_3:
		for _, item := range bags[bagIndex+0] {
			for _, item2 := range bags[bagIndex+1] {
				if item2 != item {
					continue
				}
				for _, item3 := range bags[bagIndex+2] {
					if item3 == item {
						duplicatedItem = item
						break out_3
					}
				}
			}
		}
		totalBadgePriorities += GetItemPriority(duplicatedItem)
	}

	fmt.Printf(("Part 1: %d\n"), totalPriorities)
	fmt.Printf(("Part 2: %d\n"), totalBadgePriorities)
}
