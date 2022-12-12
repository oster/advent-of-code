package main

import (
	_ "embed"
	"fmt"
)

//go:embed input.txt
var input string

const HEIGHT = 41
const WIDTH = 179

// const HEIGHT = 5
// const WIDTH = 8

func PrintHeightsMap(heightsMap [HEIGHT][WIDTH]int) {
	for _, line := range heightsMap {
		for _, c := range line {
			fmt.Printf("%c", c)
		}
		fmt.Println()
	}
}

type Point struct {
	x int
	y int
}

type Path struct {
	p      Point
	length int
}

func Contains(slice []Point, lookingFor Point) bool {
	for i := 0; i < len(slice); i++ {
		if slice[i] == lookingFor {
			return true
		}
	}
	return false
}

func FindPath(start Point, end Point, heightsMap [HEIGHT][WIDTH]int, expectedHeight int, reversed bool) int {
	// we keep these assignements there only for memory location of heightsMap?
	heightsMap[start.y][start.x] = 'a'
	heightsMap[end.y][end.x] = 'z'

	var moves [4]Point = [4]Point{{0, 1}, {1, 0}, {-1, 0}, {0, -1}}
	var visitedPositions []Point = make([]Point, 0)
	var positionsToVisit []Path = make([]Path, 0)
	var empytPath Path = Path{Point{0, 0}, 0}

	var stepAutorised func(int) bool

	if !reversed {
		stepAutorised = func(step int) bool { return step <= 1 }
		positionsToVisit = append(positionsToVisit, Path{start, 0})
	} else {
		stepAutorised = func(step int) bool { return step >= -1 }
		positionsToVisit = append(positionsToVisit, Path{end, 0})

		// in case, we check the end rather than the height
		// tmp := start
		// start = end
		// end = tmp
	}

	var current Path
	var found bool = false
	for !found && len(positionsToVisit) > 0 {
		current = positionsToVisit[0]
		positionsToVisit[0] = empytPath
		positionsToVisit = positionsToVisit[1:]

		heightOfCurrent := heightsMap[current.p.y][current.p.x]

		if heightOfCurrent == expectedHeight { // we may want to check that current == end rather than only the height
			found = true
			break
		}

		for k := 0; k < len(moves); k++ {
			move := moves[k]
			next := Point{current.p.x + move.x, current.p.y + move.y}
			if next.x >= 0 && next.x < WIDTH && next.y >= 0 && next.y < HEIGHT {
				step := heightsMap[next.y][next.x] - heightOfCurrent

				if stepAutorised(step) && !Contains(visitedPositions, next) {
					visitedPositions = append(visitedPositions, next)
					positionsToVisit = append(positionsToVisit, Path{next, current.length + 1})
				}
			}
		}
	}

	return current.length
}

func Solve() (int, int) {
	var start Point
	var end Point

	var heightsMap [HEIGHT][WIDTH]int

	for line := 0; line < HEIGHT; line++ {
		for row := 0; row < WIDTH; row++ {
			c := input[line*(WIDTH+1)+row]
			switch c {
			case 'S':
				start = Point{row, line}
				heightsMap[line][row] = 'a'
			case 'E':
				end = Point{row, line}
				heightsMap[line][row] = 'z'
			default:
				heightsMap[line][row] = int(c)
			}
		}
	}

	part1 := FindPath(start, end, heightsMap, 'z', false)

	// for part 2, we start from the end and look in reverse order
	part2 := FindPath(start, end, heightsMap, 'a', true)

	return part1, part2 // 484, 478
}
