package main

import (
	"bufio"
	"fmt"
	mapset "github.com/deckarep/golang-set/v2"
	"log"
	"os"
	"time"
)

func GetItemPriority(item rune) int {
	if item >= 'a' && item <= 'z' {
		return int(item) - int('a') + 1
	} else { // assume item >= 'A' and item <= 'Z'
		return int(item) - int('A') + 26 + 1
	}
}

func CreateSet(bag string) mapset.Set[rune] {
	m := mapset.NewSet[rune]()
	for _, c := range bag {
		m.Add(c)
	}
	return m
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
		firstCompartment, secondComparment := CreateSet(bag[:pivot]), CreateSet(bag[pivot:])

		duplicatedItem, _ := firstCompartment.Intersect(secondComparment).Pop()
		totalPriorities += GetItemPriority(duplicatedItem)
	}
	fmt.Printf(("Part 1: %d\n"), totalPriorities)

	// Part 2
	start := time.Now()
	totalBadgePriorities := 0

	for bagIndex := 0; bagIndex < len(bags); bagIndex += 3 {
		duplicatedItem, _ := (CreateSet(bags[bagIndex]).Intersect(CreateSet(bags[bagIndex+1]))).Intersect(CreateSet(bags[bagIndex+2])).Pop()
		totalBadgePriorities += GetItemPriority(duplicatedItem)
	}

	fmt.Printf(("Part 2: %d\n"), totalBadgePriorities)
	fmt.Println(time.Since(start))
}
