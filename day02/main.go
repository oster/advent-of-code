package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	totalScore, totalScorePart2 := Solve()
	fmt.Println(time.Since(start))
	fmt.Printf("Part 1: %d\n", totalScore)
	fmt.Printf("Part 2: %d\n", totalScorePart2)
}
