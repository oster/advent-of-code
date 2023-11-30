package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	start1, start2 := Solve()
	fmt.Println(time.Since(start))
	fmt.Printf(("Part 1: %d\n"), start1)
	fmt.Printf(("Part 2: %d\n"), start2)
}
