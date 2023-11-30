package main

import (
	"bufio"
	"log"
	"os"

	mapset "github.com/deckarep/golang-set/v2"
)

func CreateSet(bag string) mapset.Set[rune] {
	m := mapset.NewSet[rune]()
	for _, c := range bag {
		m.Add(c)
	}
	return m
}

func SolveWithSet() (int, int) {
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
		firstCompartment, secondComparment := CreateSet(bag[:pivot]), CreateSet(bag[pivot:])

		duplicatedItem, _ := firstCompartment.Intersect(secondComparment).Pop()
		totalPriorities += GetItemPriority(duplicatedItem)
	}

	// Part 2
	totalBadgePriorities := 0

	for bagIndex := 0; bagIndex < len(bags); bagIndex += 3 {
		duplicatedItem, _ := (CreateSet(bags[bagIndex]).Intersect(CreateSet(bags[bagIndex+1]))).Intersect(CreateSet(bags[bagIndex+2])).Pop()
		totalBadgePriorities += GetItemPriority(duplicatedItem)
	}

	return totalPriorities, totalBadgePriorities
}
