package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"strings"
)

//go:embed input.txt
var input string

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

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

func PrintGrid(grid map[Pos]bool) {
	var xMin int = math.MaxInt
	var yMin int = math.MaxInt
	var xMax int = math.MinInt
	var yMax int = math.MinInt

	for pos := range grid {
		xMin = min(xMin, pos.x)
		yMin = min(yMin, pos.y)
		xMax = max(xMax, pos.x)
		yMax = max(yMax, pos.y)
	}

	// add empty borders
	xMin--
	xMax++
	yMin--
	yMax++

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

func ParseInput() (elvesPositions map[Pos]bool) {
	elvesPositions = make(map[Pos]bool)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	// xMin = 0
	// yMin = 0

	y := 0
	for scanner.Scan() {
		line := scanner.Text()
		// xMax = max(xMax, len(scanner.Text())-1)
		for x, c := range line {
			if c == '#' {
				elvesPositions[Pos{x, y}] = true
			}
		}
		y++
	}
	// yMax = y - 1

	return elvesPositions
}

type Elf struct {
	current             Pos
	next                Pos
	directionToConsider int
}

type Direction Pos // just a nice alias

var N = Direction{0, -1}
var NE = Direction{1, -1}
var E = Direction{1, 0}
var SE = Direction{1, 1}
var S = Direction{0, 1}
var SW = Direction{-1, 1}
var W = Direction{-1, 0}
var NW = Direction{-1, -1}

var directions [8]Direction = [8]Direction{N, NE, E, SE, S, SW, W, NW}
var directionsStrings [8]string = [8]string{"N", "NE", "E", "SE", "S", "SW", "W", "NW"}

func GetDirectionAsString(directionIndex int) string {
	return directionsStrings[directionIndex]
}

func neighborPos(pos Pos, direction Direction) (neighbor Pos) {
	neighbor = pos
	neighbor.x += direction.x
	neighbor.y += direction.y
	return neighbor
}

func PrintElves(elves []*Elf) {
	fmt.Print("elves: ")
	for idx, elf := range elves {
		if idx != 0 {
			fmt.Print(", ")
		}
		fmt.Printf("%+v", *elf)
	}
	fmt.Println()
}

func CountEmptyTiles(grid map[Pos]bool) (emptyTilesCount int) {
	var xMin int = math.MaxInt
	var yMin int = math.MaxInt
	var xMax int = math.MinInt
	var yMax int = math.MinInt

	for pos := range grid {
		xMin = min(xMin, pos.x)
		yMin = min(yMin, pos.y)
		xMax = max(xMax, pos.x)
		yMax = max(yMax, pos.y)
	}

	emptyTilesCount = (yMax-yMin+1)*(xMax-xMin+1) - len(grid)
	return emptyTilesCount
}

// func CountEmptyTilesOld(grid map[Pos]bool) (emptyTilesCount int) {
// 	var xMin int = math.MaxInt
// 	var yMin int = math.MaxInt
// 	var xMax int = math.MinInt
// 	var yMax int = math.MinInt

// 	for pos := range grid {
// 		xMin = min(xMin, pos.x)
// 		yMin = min(yMin, pos.y)
// 		xMax = max(xMax, pos.x)
// 		yMax = max(yMax, pos.y)
// 	}

// 	for y := yMin; y <= yMax; y++ {
// 		for x := xMin; x <= xMax; x++ {
// 			if _, ok := grid[Pos{x, y}]; !ok {
// 				emptyTilesCount++
// 			}
// 		}
// 	}
// 	return emptyTilesCount
// }

func PlayRound(round int, elves []*Elf, elvesPositions map[Pos]bool) (newElvesPositions map[Pos]bool, howManyElvesMoves int) {
	// first half of round
	var proposals map[Pos]int = make(map[Pos]int)

	for _, elf := range elves {
		elfPos := elf.current

		elvesInTheNeighborhood := 0
		for _, direction := range directions {
			if _, ok := elvesPositions[neighborPos(elfPos, direction)]; ok {
				elvesInTheNeighborhood++
			}
		}

		if elvesInTheNeighborhood == 0 {
			// don't move during that round
			elf.next = elf.current
			// fmt.Printf("%+v will not move (stay at %+v)\n", elf.current, elf.next)
		} else {
			// mayMove := false

			for idxQuadrantIndex := 0; idxQuadrantIndex < 4; idxQuadrantIndex++ {
				quadrantIndex := quadrantIndexes[(round+idxQuadrantIndex)%4]
				// fmt.Printf("elves will consider %s direction (%d) first\n", GetDirectionAsString(quadrantIndex), quadrantIndex)

				elvesInTheQuadrant := 0
				for quadrantShit := -1; quadrantShit <= 1; quadrantShit++ {
					directionIndex := (quadrantIndex + quadrantShit + 8) % 8
					// fmt.Println("directionIndex:", directionIndex)
					direction := directions[directionIndex]
					nPos := neighborPos(elfPos, direction)
					// fmt.Printf("  checking %s (at %+v) of %+v\n", GetDirectionAsString(directionIndex), nPos, elf.current)
					if _, ok := elvesPositions[nPos]; ok {
						elvesInTheQuadrant++
					}
				}
				// fmt.Printf("there are %d elves in the %s quadrant of %+v\n", elvesInTheQuadrant, GetDirectionAsString(quadrantIndex), elf.current)
				if elvesInTheQuadrant == 0 {
					// mayMove = true
					elf.next = neighborPos(elfPos, directions[quadrantIndex])
					// fmt.Printf("%+v proposed to move to %s (%+v)\n", elf.current, GetDirectionAsString(quadrantIndex), elf.next)
					// store proposal
					_, ok := proposals[elf.next]
					if !ok {
						proposals[elf.next] = 1
					} else {
						proposals[elf.next]++
					}
					break
				} else {
					// fmt.Println("so not move")
					elf.next = elf.current
				}
			}
			// if !mayMove {
			// 	fmt.Printf("%+v will not move\n", elf.current)
			// }
		}
	}

	// fmt.Printf("proposals: %+v\n", proposals)
	// PrintGrid(elvesPositions)

	// second half of the round
	for _, elf := range elves {
		// fmt.Printf("%+v ... proposal count=%d\n", *elf, proposals[elf.next])
		if proposals[elf.next] == 1 {
			// effectively move
			// fmt.Printf("%+v will move to %+v\n", elf.current, elf.next)
			delete(elvesPositions, elf.current)
			elf.current = elf.next
			elvesPositions[elf.current] = true
			howManyElvesMoves++
		}
	}

	// fmt.Printf("== End Round %d ==\n", round+1)
	// PrintGrid(elvesPositions)
	// fmt.Println("empty tiles: ", CountEmptyTiles(elvesPositions))

	return elvesPositions, howManyElvesMoves
}

var quadrantIndexes [4]int = [4]int{0, 4, 6, 2} // {N, S, W, E}

func Part1(maxRound int, elvesPositions map[Pos]bool) int {
	var elves []*Elf = make([]*Elf, 0)

	for elfPos := range elvesPositions {
		elves = append(elves, &Elf{current: elfPos})
	}

	// fmt.Printf("== Initial State ==\n")
	// PrintGrid(elvesPositions)

	for round := 0; round < maxRound; round++ {
		PlayRound(round, elves, elvesPositions)
	}

	// fmt.Printf("== Final Round %d ==\n", maxRound)
	// PrintGrid(elvesPositions)
	// fmt.Println("empty tiles: ", CountEmptyTiles(elvesPositions))

	return CountEmptyTiles(elvesPositions)
}

func Part2(elvesPositions map[Pos]bool) int {
	var elves []*Elf = make([]*Elf, 0)

	for elfPos := range elvesPositions {
		elves = append(elves, &Elf{current: elfPos})
	}

	round := 0
	howManyElvesMoves := len(elves)
	for howManyElvesMoves > 0 {
		elvesPositions, howManyElvesMoves = PlayRound(round, elves, elvesPositions)
		round++
	}

	return round
}

func Solve() (int, int) {
	var originalElvesPositions map[Pos]bool = make(map[Pos]bool)
	originalElvesPositions = ParseInput()

	// make a copy for Part 2
	var elvesPositions map[Pos]bool = make(map[Pos]bool)
	for k, v := range originalElvesPositions {
		elvesPositions[k] = v
	}

	part1 := Part1(10, elvesPositions)     // 110, 3788
	part2 := Part2(originalElvesPositions) // 20, 921

	return part1, part2
}
