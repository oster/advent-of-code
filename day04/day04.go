package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	dataFile, err := os.Open("input.txt")
	if err != nil {
		log.Fatal("failed to open data file")
	}

	fully_overlap_count := 0
	partial_overlap_count := 0

	type IdRange struct {
		start int
		end   int
	}

	var elf1 IdRange
	var elf2 IdRange

	fileScanner := bufio.NewScanner(dataFile)
	for fileScanner.Scan() {
		fmt.Sscanf(fileScanner.Text(), "%d-%d,%d-%d", &elf1.start, &elf1.end, &elf2.start, &elf2.end)

		if (elf1.start <= elf2.start && elf1.end >= elf2.end) || (elf2.start <= elf1.start && elf2.end >= elf1.end) {
			fully_overlap_count++
		}

		if (elf1.end >= elf2.start && elf1.start <= elf2.end) || (elf2.end >= elf1.start && elf2.start <= elf1.end) {
			partial_overlap_count++
		}
	}

	dataFile.Close()

	fmt.Printf(("Part 1: %d\n"), fully_overlap_count)
	fmt.Printf(("Part 2: %d\n"), partial_overlap_count)
}
