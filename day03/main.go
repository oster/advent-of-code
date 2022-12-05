package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	totalPriorities, totalBadgePriorities := SolveEmbed()
	fmt.Println(time.Since(start))
	fmt.Printf("Part 1: %d\n", totalPriorities)
	fmt.Printf("Part 2: %d\n", totalBadgePriorities)
}
