package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"os"
	"strings"
)

//go:embed sample.txt
var input string

var facesDescriptor [6][2]int = [6][2]int{{0, 8}, {4, 0}, {4, 4}, {4, 8}, {8, 8}, {8, 12}} // sample
// var facesDescriptor [6][2]int = [6][2]int{{0, 50}, {0, 100}, {50, 50}, {100, 0}, {100, 50}, {150, 0}} // input

type TransDestination struct {
	face     int
	rotation int
}
type Transitions [6][4]TransDestination

var transitions Transitions = Transitions{
	{TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}}, // from face 0 to face x (E,S,W,N)
	{TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}}, // from face 1 to face x
	{TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}}, // from face 2 to face x
	{TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}}, // from face 3 to face x
	{TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}}, // from face 4 to face x
	{TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}, TransDestination{face: 0, rotation: 0}}} // from face 5 to face x

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

func ParseMoveLine(movesLine string) (moves []Move) {
	moves = make([]Move, 0)

	value := 0
	var move Move

	for idx := 0; idx < len(movesLine); idx++ {
		char := movesLine[idx]
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

	return moves
}

func ParseInput() (data [][]byte, rows map[int]Interval, columns map[int]Interval, moves []Move) {
	rows = make(map[int]Interval)
	columns = make(map[int]Interval)
	data = make([][]byte, 0)

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

	moves = ParseMoveLine(lastLine)

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

type Face struct {
	data [][]byte
	size int
}

func (current *Face) Print() {
	for y := 0; y < current.size; y++ {
		for x := 0; x < current.size; x++ {
			fmt.Printf("%c", current.data[y][x])
		}
		fmt.Println()
	}
}

type Cube struct {
	faces [6]Face
	size  int
}

func (current *Cube) Print() {
	for faceId := 0; faceId < 6; faceId++ {
		current.faces[faceId].Print()
		fmt.Println()
	}
}

func ParseInputPart2(size int, facesDescriptor [6][2]int) (cube Cube, moves []Move) {
	cube = Cube{size: size}

	lines := strings.Split(input, "\n")

	for faceId := 0; faceId < 6; faceId++ {
		var someFace Face = Face{size: size}
		someFace.data = make([][]byte, size)

		startY := facesDescriptor[faceId][0]
		startX := facesDescriptor[faceId][1]
		for y := 0; y < size; y++ {
			someFace.data[y] = make([]byte, size)
			for x := 0; x < size; x++ {
				someFace.data[y][x] = lines[y+startY][x+startX]
			}
		}
		cube.faces[faceId] = someFace
	}

	moves = ParseMoveLine(lines[len(lines)-2])
	return cube, moves
}

type Pos3D struct {
	x    int
	y    int
	face int
}

func Part2(cube Cube, moves []Move) int {
	var current Pos3D = Pos3D{0, 0, 0}
	facing := 0 // heading to EAST

	if cube.faces[current.face].data[current.y][current.x] != '.' {
		panic("wrong starting coord:" + fmt.Sprintf("%v", current))
	}

	for _, move := range moves {

		if move.length == 0 {
			// only rotation
			facing = (facing + move.rotation + HEADINGS_SIZE) % HEADINGS_SIZE
			continue
		}

		var heading Direction = HEADINGS[facing]

		var next Pos3D = current

		for step := 0; step < move.length; step++ {
			heading = HEADINGS[facing]

			next.x = (current.x + heading.x)
			if next.x >= cube.size {
				// switch to another face
				next.x = 0
			} else if next.x < 0 {
				// switch to another face
				next.x = cube.size - 1
			}

			next.y = (current.y + heading.y)
			if next.y >= cube.size {
				// switch to anoter face
				next.y = 0
			} else if next.y < 0 {
				// switch to anoter face
				next.y = cube.size - 1
			}

			fmt.Printf("%c virtually at (%d,%d)\n", GetFacingAsChar(facing), next.x, next.y)
			if cube.faces[next.face].data[next.y][next.x] == '.' {
				// mark the last position
				cube.faces[current.face].data[current.y][next.x] = GetFacingAsChar(facing)
				current = next
			} else {
				// can't move
				break
			}
		}

		fmt.Println()
		cube.faces[current.face].Print()
		os.Stdin.Read(make([]byte, 1))
	}

	return 1000*(current.y+1) + 4*(current.x+1) + facing

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

	part1 := Part1(data, rows, columns, moves) // 6032, 109094

	// var cube Cube
	// cube, moves = ParseInputPart2(4, facesDescriptor) // sample.txt - (startY, startX, startY+size, startX+size)

	//TODO: add transitions between faces
	// (faceIdx, direction) -> faceIdx (do we need to change the heading also?)

	//	cube, moves = ParseInputPart2(50, facesDescriptor) // input.txt

	// cube.Print()
	// fmt.Println(moves)

	// part2 := Part2(cube, moves)
	part2 := 0 // 5031, ?
	return part1, part2
}
