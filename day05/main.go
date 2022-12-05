package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	stacks, stacks2 := Solve()
	fmt.Println(time.Since(start))

	PrintTopOfStacks(stacks)
	PrintTopOfStacks(stacks2)
}
