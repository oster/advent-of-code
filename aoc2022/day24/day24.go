package main

import (
	_ "embed"
	"fmt"
	"strings"

	"github.com/edwingeng/deque/v2"
)

//go:embed input.txt
var input string

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func pgcd(a int, b int) int {
	if b == 0 {
		return a
	}
	return pgcd(b, a%b)
}

func ppcm(a int, b int) int {
	return abs(a*b) / pgcd(a, b)
}

type Pos struct {
	x int
	y int
}

var width int
var height int
var start Pos
var end Pos
var grid [][]byte

var blizzards []*Blizzard

type Blizzard struct {
	x         int
	y         int
	direction Pos
	char      byte
}

var NORTH = Pos{0, -1}
var SOUTH = Pos{0, 1}
var EAST = Pos{1, 0}
var WEST = Pos{-1, 0}

var DIRECTIONS [4]Pos = [4]Pos{NORTH, SOUTH, EAST, WEST}

func PrintGridAtTime(time int) {
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			if present := IsBlizzardAtTime(time, Pos{x, y}); present {
				fmt.Printf("W")
			} else {
				fmt.Printf("%c", grid[y][x])
			}
		}
		fmt.Println()
	}
}

func PrintMarkedGridAtTime(time int, marker Pos) {
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {

			if x == marker.x && y == marker.y {
				fmt.Print("*")
				continue
			}

			if present := IsBlizzardAtTime(time, Pos{x, y}); present {
				fmt.Printf("W")
			} else {
				fmt.Printf("%c", grid[y][x])
			}
		}
		fmt.Println()
	}
}

func MoveBlizzards() {
	for i := 0; i < len(blizzards); i++ {
		blizz := blizzards[i]
		// fmt.Printf("%+v (before)\n", blizz)
		blizz.x = (blizz.x-1+blizz.direction.x+width-2)%(width-2) + 1
		blizz.y = (blizz.y-1+blizz.direction.y+height-2)%(height-2) + 1
		// fmt.Printf("%+v (after)\n", blizz)
	}
}

var blizzardsAtAllTime []map[Pos]bool
var PRECOMPUTATION bool = false

func ComputeBlizzardAtAllTime() {
	if !PRECOMPUTATION {

		// fmt.Println("starting computation of blizzards")
		ppcm := ppcm(width, height)
		// fmt.Println(ppcm)

		blizzardsAtAllTime = make([]map[Pos]bool, ppcm)

		blizzardsAtAllTime[0] = make(map[Pos]bool)
		for i := 0; i < len(blizzards); i++ {
			blizz := blizzards[i]
			blizzardsAtAllTime[0][Pos{blizz.x, blizz.y}] = true
		}

		for t := 1; t < ppcm; t++ {
			blizzardsAtAllTime[t] = make(map[Pos]bool)
			for i := 0; i < len(blizzards); i++ {
				blizz := blizzards[i]
				// fmt.Printf("%+v (before)\n", blizz)
				blizz.x = (blizz.x-1+blizz.direction.x+width-2)%(width-2) + 1
				blizz.y = (blizz.y-1+blizz.direction.y+height-2)%(height-2) + 1
				// fmt.Printf("%+v (after)\n", blizz)
				blizzardsAtAllTime[t][Pos{blizz.x, blizz.y}] = true
			}
		}
		PRECOMPUTATION = true
	}
	// fmt.Println("end of computation of blizzards")
}

func IsBlizzardAtTime(time int, pos Pos) bool {
	_, present := blizzardsAtAllTime[time%len(blizzardsAtAllTime)][pos]
	return present
}

func ParseInput() {
	lines := strings.Split(input, "\n")

	height = len(lines) - 1
	width = len(lines[0])

	blizzards = make([]*Blizzard, 0)

	grid = make([][]byte, height)
	for y := 0; y < height; y++ {
		grid[y] = make([]byte, width)
		for x := 0; x < width; x++ {
			switch lines[y][x] {
			case '#', '.':
				grid[y][x] = lines[y][x] // useless ???
			case '>':
				blizzards = append(blizzards, &Blizzard{x, y, EAST, '>'})
				grid[y][x] = '.' // useless
			case '<':
				blizzards = append(blizzards, &Blizzard{x, y, WEST, '<'})
				grid[y][x] = '.' // useless
			case '^':
				blizzards = append(blizzards, &Blizzard{x, y, NORTH, '^'})
				grid[y][x] = '.' // useless
			case 'v':
				blizzards = append(blizzards, &Blizzard{x, y, SOUTH, 'v'})
				grid[y][x] = '.' // useless
			}
		}
	}

	// store Start and End positions
	for x := 0; x < width; x++ {
		if grid[0][x] == '.' {
			start = Pos{x, 0}
		}
		if grid[height-1][x] == '.' {
			end = Pos{x, height - 1}
		}
	}
}

func Part1() int {
	ComputeBlizzardAtAllTime()

	// for t := 0; t < ppcm(width, height); t++ {
	// 	PrintGridAtTime(t)
	// 	fmt.Println()
	// }

	// for t := 0; t <= 18; t++ {
	// 	PrintGrid()
	// 	MoveBlizzards()
	// 	fmt.Println()
	// }

	elapsedTime := Part1BFSSearch(start, end, State{0, start})
	return elapsedTime
}

type State struct {
	time       int
	currentPos Pos
}

func GetNextPositions(current State) (nextPositions []Pos) {
	// fmt.Printf("++ GetNextPositions(%+v)\n", current)
	nextPositions = make([]Pos, 0)
	currentPos := current.currentPos
	for _, direction := range DIRECTIONS {
		nextX := currentPos.x + direction.x
		nextY := currentPos.y + direction.y
		nextPos := Pos{nextX, nextY}

		if nextX >= 0 && nextX < width && nextY >= 0 && nextY < height && grid[nextY][nextX] == '.' && !IsBlizzardAtTime(current.time+1, nextPos) {
			nextPositions = append(nextPositions, nextPos)
		}
	}
	// wait one turn, if no blizzard will come
	if !IsBlizzardAtTime(current.time+1, currentPos) {
		nextPositions = append(nextPositions, Pos{currentPos.x, currentPos.y})
	}

	return nextPositions
}

func PrintPath(visited map[State]State, end State, startPos Pos) {

	fmt.Println(end)
	previousState, ok := visited[end]

	for ok {
		fmt.Println(previousState)
		previousState, ok = visited[previousState]
	}
}

func Part1BFSSearch(start Pos, end Pos, initialState State) int {

	var states *deque.Deque[State] = deque.NewDeque[State]()
	// var visited map[State]bool = make(map[State]bool)
	var visited map[State]State = make(map[State]State)

	states.PushBack(initialState)

	// fmt.Printf("%+v\n", initialState)
	// PrintMarkedGridAtTime(initialState.time, initialState.currentPos)
	// fmt.Println()

	for !states.IsEmpty() {
		currentState := states.PopFront()
		// fmt.Printf("++ Popping = %+v\n", currentState)

		for _, nextPos := range GetNextPositions(currentState) {
			newState := State{currentState.time + 1, nextPos}

			if newState.currentPos.x == end.x && newState.currentPos.y == end.y {
				// fmt.Println("++ Found!")
				// fmt.Printf("%+v\n", newState)

				// PrintMarkedGridAtTime(newState.time, newState.currentPos)
				visited[newState] = currentState

				// PrintPath(visited, newState, start)

				return newState.time
			}

			if _, ok := visited[newState]; !ok {
				visited[newState] = currentState
				states.PushBack(newState)
				// fmt.Printf("++ Pushing = %+v\n", newState)

				// fmt.Printf("%+v\n", newState)
				// PrintMarkedGridAtTime(newState.time, newState.currentPos)
				// fmt.Println()
			}
		}
	}

	return -1
}

func Part2() int {
	time := Part1()
	time = Part1BFSSearch(end, start, State{time, end})
	time = Part1BFSSearch(start, end, State{time, start})

	return time
}

func Solve() (int, int) {
	ParseInput()
	// PrintGrid()
	// fmt.Printf("start: %+v, end: %+v\n", start, end)
	// fmt.Println(blizzards)

	part1 := Part1() // 18, 279
	part2 := Part2() // 54, 762
	return part1, part2
}
