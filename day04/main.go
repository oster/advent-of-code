package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	fullyOverlapCount, partialOverlapCount := SolveEmbed()
	fmt.Println(time.Since(start))
	fmt.Printf(("Part 1: %d\n"), fullyOverlapCount)
	fmt.Printf(("Part 2: %d\n"), partialOverlapCount)
}
