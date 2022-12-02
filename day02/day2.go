package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	// A: Rock, B: Paper, C: Scissors
	// X: Rock, Y: Paper, Z: Scissors
	// ->
	// score
	yours_vs_mine := map[string]int{
		"A X": 3 + 1,
		"B X": 0 + 1,
		"C X": 6 + 1,
		"B Y": 3 + 2,
		"A Y": 6 + 2,
		"C Y": 0 + 2,
		"A Z": 0 + 3,
		"B Z": 6 + 3,
		"C Z": 3 + 3}

	// A: Rock, B: Paper, C: Scissors
	// X: lose, Y: draw, Z:win
	// ->
	// X: Rock, Y: Paper, Z: Scissors, score

	type Pair struct {
		string
		int
	}

	yours_expected := map[string]Pair{
		"A X": Pair{"Z", 3 + 0},
		"A Y": Pair{"X", 1 + 3},
		"A Z": Pair{"Y", 2 + 6},
		"B X": Pair{"X", 1 + 0},
		"B Y": Pair{"Y", 2 + 3},
		"B Z": Pair{"Z", 3 + 6},
		"C X": Pair{"Y", 2 + 0},
		"C Y": Pair{"Z", 3 + 3},
		"C Z": Pair{"X", 1 + 6}}

	dataFile, err := os.Open("input.txt")
	if err != nil {
		log.Fatal("failed to open data file")
	}

	total_score := 0
	total_score_part2 := 0
	round_outcome := 0

	fileScanner := bufio.NewScanner(dataFile)
	for fileScanner.Scan() {
		line := fileScanner.Text()
		round_outcome = yours_vs_mine[line]
		total_score += round_outcome

		total_score_part2 += yours_expected[line].int
	}

	dataFile.Close()

	fmt.Printf(("Part 1: %d\n"), total_score)
	fmt.Printf(("Part 2: %d\n"), total_score_part2)
}
