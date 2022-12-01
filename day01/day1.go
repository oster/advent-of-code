package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

func main() {

	dataFile, err := os.Open("input.txt")
	if err != nil {
		log.Fatal("failed to open data file")
	}

	calories_by_elfs := make([][]int, 0)

	fileScanner := bufio.NewScanner(dataFile)
	var elf []int = make([]int, 0)
	for fileScanner.Scan() {
		line := fileScanner.Text()
		if len(line) == 0 {
			calories_by_elfs = append(calories_by_elfs, elf)
			elf = make([]int, 0)
		} else {
			value := 0
			value, _ = strconv.Atoi(line)
			elf = append(elf, value)
		}
	}
	dataFile.Close()

	max_calories := 0
	var sums_of_calories []int = make([]int, len(calories_by_elfs))

	for _, calories := range calories_by_elfs {
		sum := 0
		for _, calorie := range calories {
			sum += calorie
		}
		sums_of_calories = append(sums_of_calories, sum)

		if sum > max_calories {
			max_calories = sum
		}
	}
	fmt.Printf(("Part 1: %d\n"), max_calories)

	sort.Slice(sums_of_calories, func(i, j int) bool {
		return sums_of_calories[i] > sums_of_calories[j]
	})

	sum_of_three_with_most_calories := sums_of_calories[0] + sums_of_calories[1] + sums_of_calories[2]
	fmt.Printf("Part 2: %d\n", sum_of_three_with_most_calories)
}
