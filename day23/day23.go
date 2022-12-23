package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"strings"
)

//go:embed sample.txt
var input string

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

type Pos struct {
	x int
	y int
}

var grid map[Pos]bool = make(map[Pos]bool)

var xMin int = math.MaxInt
var yMin int = math.MaxInt
var xMax int = math.MinInt
var yMax int = math.MinInt

func PrintGrid(grid map[Pos]bool) {
	for y := yMin; y <= yMax; y++ {
		for x := xMin; x <= xMax; x++ {
			if _, ok := grid[Pos{x, y}]; ok {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}

}

func ParseInput() (grid map[Pos]bool) {
	grid = make(map[Pos]bool)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	xMin = 0
	yMin = 0

	y := 0
	for scanner.Scan() {
		line := scanner.Text()
		xMax = max(xMax, len(scanner.Text())-1)
		for x, c := range line {
			if c == '#' {
				grid[Pos{x, y}] = true
			}
		}
		y++
	}
	yMax = y - 1

	return grid
}

func Part1() int {
	return 0
}

func Part2() int {
	return 0
}

func Solve() (int, int) {
	var grid map[Pos]bool = make(map[Pos]bool)
	grid = ParseInput()

	PrintGrid(grid)

	part1 := 0
	part2 := 0
	return part1, part2
}
