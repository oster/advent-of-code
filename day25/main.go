package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	start1 := Solve()
	fmt.Println(time.Since(start))
	fmt.Printf(("Part 1: %s\n"), start1)
}
