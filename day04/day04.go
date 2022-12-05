package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func Solve() (int, int) {
	dataFile, err := os.Open("input.txt")
	if err != nil {
		log.Fatal("failed to open data file")
	}

	fullyOverlapCount := 0
	partialOverlapCount := 0

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
			fullyOverlapCount++
		}

		if (elf1.end >= elf2.start && elf1.start <= elf2.end) || (elf2.end >= elf1.start && elf2.start <= elf1.end) {
			partialOverlapCount++
		}
	}

	dataFile.Close()

	return fullyOverlapCount, partialOverlapCount
}
