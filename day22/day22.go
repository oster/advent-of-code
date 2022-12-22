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

type Interval struct {
	min int
	max int
}

type Direction Pos // just a nice alias

var NORTH = Direction{0, -1}
var EAST = Direction{1, 0}
var SOUTH = Direction{0, 1}
var WEST = Direction{-1, 0}

var HEADINGS [4]Direction = [4]Direction{EAST, SOUTH, WEST, NORTH}
var HEADINGS_SIZE = len(HEADINGS)

var FACING_CHAR [4]byte = [4]byte{'>', 'v', '<', '^'}

func GetFacingAsChar(facing int) byte {
	return FACING_CHAR[facing]
}

type Move struct {
	length   int
	rotation int
}

func ParseInput() (data [][]byte, rows map[int]Interval, columns map[int]Interval, moves []Move) {
	rows = make(map[int]Interval)
	columns = make(map[int]Interval)
	data = make([][]byte, 0)
	moves = make([]Move, 0)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	rowIdx := 0
	for scanner.Scan(); len(scanner.Text()) > 1; scanner.Scan() {
		line := strings.TrimRight(scanner.Text(), "\n")

		var rowInterval Interval = Interval{min: math.MaxInt, max: math.MinInt}

		var dataLine []byte = make([]byte, 0)
		var columnIdx = 0
		for columnIdx = 0; columnIdx < len(line); columnIdx++ {
			columnInterval, ok := columns[columnIdx]
			if !ok {
				columnInterval = Interval{min: math.MaxInt, max: math.MinInt}
			}

			char := line[columnIdx]
			if char == '.' || char == '#' {
				dataLine = append(dataLine, char)
				rowInterval.min = min(columnIdx, rowInterval.min)
				rowInterval.max = max(columnIdx, rowInterval.min)
				columnInterval.min = min(rowIdx, columnInterval.min)
				columnInterval.max = max(rowIdx, columnInterval.min)
				columns[columnIdx] = columnInterval
			}
		}
		data = append(data, dataLine)
		rows[rowIdx] = rowInterval
		rowIdx++
	}

	scanner.Scan()
	lastLine := scanner.Text()

	value := 0
	var move Move

	for idx := 0; idx < len(lastLine); idx++ {
		char := lastLine[idx]
		if char >= '0' && char <= '9' {
			value = value*10 + int(char-'0')
			continue
		} else {
			moves = append(moves, Move{length: value, rotation: 0})
		}

		switch char {
		case 'R':
			move = Move{length: 0, rotation: 1}
			value = 0
		case 'L':
			move = Move{length: 0, rotation: -1}
			value = 0
		default:
			panic("invalid rotation instruction in puzzle description")
		}
		moves = append(moves, move)
	}

	if value != 0 {
		moves = append(moves, Move{length: value, rotation: 0})
	}
	return data, rows, columns, moves
}

func PrintMap(data [][]byte, rows map[int]Interval, columns map[int]Interval) {
	// need to be rewritten since we change the datastructures in the meantime...
	for rowIndex := 0; rowIndex < len(data); rowIndex++ {
		for columnIndex := 0; columnIndex < rows[rowIndex].min; columnIndex++ {
			fmt.Print(" ")
		}
		for columnIndex := rows[rowIndex].min; columnIndex < rows[rowIndex].max; columnIndex++ {
			fmt.Printf("%c", data[rowIndex][columnIndex-rows[rowIndex].min])
		}
		fmt.Println()
	}
}

func Part1(data [][]byte, rows map[int]Interval, columns map[int]Interval, moves []Move) int {
	var current Pos = Pos{rows[0].min, columns[rows[0].min].min} // top-left most open tile
	facing := 0                                                  // facing to Right

	// fmt.Println("current.x:", current.x, "current.y:", current.y)

	if data[current.y][current.x-rows[current.y].min] != '.' {
		panic("wrong starting coord:" + fmt.Sprintf("%v", current))
	}

	// data[current.y][current.x-rows[current.y].min] = 'S'
	// fmt.Printf("%c at (%d,%d)\n", GetFacingAsChar(facing), current.x, current.y)
	// PrintMap(data, rows, columns)

	for _, move := range moves {

		if move.length == 0 {
			// only rotation
			facing = (facing + move.rotation + HEADINGS_SIZE) % HEADINGS_SIZE
			continue
		}

		var heading Direction = HEADINGS[facing]

		var next Pos = current
		for step := 0; step < move.length; step++ {
			heading = HEADINGS[facing]

			next.x = (current.x + heading.x)
			if next.x > rows[next.y].max {
				next.x = rows[next.y].min
			} else if next.x < rows[next.y].min {
				next.x = rows[next.y].max
			}

			next.y = (current.y + heading.y)
			if next.y > columns[next.x].max {
				next.y = columns[next.x].min
			} else if next.y < columns[next.x].min {
				next.y = columns[next.x].max
			}

			// fmt.Printf("%c virtually at (%d,%d)\n", GetFacingAsChar(facing), next.x, next.y)
			if data[next.y][next.x-rows[next.y].min] == '.' {
				// mark the last position
				// data[current.y][next.x-rows[next.y].min] = GetFacingAsChar(facing)
				current = next
			} else {
				// can't move
				break
			}
		}
		// fmt.Println()
		// PrintMap(data, rows, columns)
		// os.Stdin.Read(make([]byte, 1))
	}

	// fmt.Printf("x: %d, y: %d, facing: %d\n", current.x, current.y, facing)
	// expected values for sample
	// current.x = 7
	// current.y = 5
	// facing = 0
	// fmt.Printf("x: %d, y: %d, facing: %d  (expectations)\n", current.x, current.y, facing)

	return 1000*(current.y+1) + 4*(current.x+1) + facing
}

func Part2() int {
	return 0
}

func Solve() (int, int) {
	var data [][]byte
	var moves []Move
	var rows map[int]Interval
	var columns map[int]Interval
	data, rows, columns, moves = ParseInput()

	// fmt.Println("rows intervals: ", rows)
	// fmt.Println("columns intervals: ", columns)
	// fmt.Println()
	// PrintMap(data, rows, columns)
	// fmt.Println()
	// fmt.Println(moves)

	part1 := Part1(data, rows, columns, moves)
	part2 := 0
	return part1, part2
}
