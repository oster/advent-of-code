package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	maxCalories, sumOfThreeWithMostCalories := Solve()
	fmt.Println(time.Since(start))
	fmt.Printf("Part 1: %d\n", maxCalories)
	fmt.Printf("Part 2: %d\n", sumOfThreeWithMostCalories)
}
