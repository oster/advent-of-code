package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"os"
	"strings"
)

//go:embed input.txt
var input string

type TransDestination struct {
	face     int
	rotation int
}
type Transitions [6][4]TransDestination

var transitions Transitions

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

var EAST_INDEX = 0
var SOUTH_INDEX = 1
var WEST_INDEX = 2
var NORTH_INDEX = 3

var FACING_CHAR [4]byte = [4]byte{'>', 'v', '<', '^'}

func GetDirectionIndex(direction Direction) int {
	switch direction {
	case NORTH:
		return NORTH_INDEX
	case EAST:
		return EAST_INDEX
	case SOUTH:
		return SOUTH_INDEX
	case WEST:
		return WEST_INDEX
	}

	panic("unknown direction")
}

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
	id   int
}

func (current *Face) Print() {
	fmt.Printf("== Face %d\n", current.id)
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
		var someFace Face = Face{size: size, id: faceId}
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

func Part2(cube Cube, moves []Move, facesDescriptor [6][2]int) int {
	var current Pos3D = Pos3D{x: 0, y: 0, face: 0}
	facing := EAST_INDEX

	if cube.faces[current.face].data[current.y][current.x] != '.' {
		panic("wrong starting coord:" + fmt.Sprintf("%v", current))
	}

	for _, move := range moves {

		if move.length == 0 {
			// only rotation
			facing = (facing + move.rotation + HEADINGS_SIZE) % HEADINGS_SIZE
			cube.faces[current.face].data[current.y][current.x] = GetFacingAsChar(facing)
			continue
		}

		var next Pos3D = current

		for step := 0; step < move.length; step++ {
			heading := HEADINGS[facing]

			next.x = (current.x + heading.x)
			next.y = (current.y + heading.y)

			// // we need to wrap and switch face
			needFaceSwitching := false
			if next.x >= cube.size {
				next.x = 0
				needFaceSwitching = true
			}
			if next.x < 0 {
				next.x = cube.size - 1
				needFaceSwitching = true
			}
			if next.y >= cube.size {
				next.y = 0
				needFaceSwitching = true
			}
			if next.y < 0 {
				next.y = cube.size - 1
				needFaceSwitching = true
			}

			var oldFacing = facing
			if needFaceSwitching {
				next, facing = SwitchFace(next, heading, facing, cube)
			}

			// fmt.Printf("%c potentially at (%d,%d) on Face %d\n", GetFacingAsChar(facing), next.x, next.y, next.face)
			if cube.faces[next.face].data[next.y][next.x] != '#' {
				// mark the last position
				// fmt.Printf("marking: %+v width heading %c\n", current, GetFacingAsChar(oldFacing))
				cube.faces[current.face].data[current.y][current.x] = GetFacingAsChar(oldFacing)
				// cube.faces[current.face].Print()
				current = next
				cube.faces[next.face].data[next.y][next.x] = GetFacingAsChar(facing)
			} else {
				// can't move
				facing = oldFacing
				break

			}

			// fmt.Println()
			// cube.faces[current.face].Print()
			// WaitKeyPress()
		}

	}

	// fmt.Printf("row: %d, column: %d, face: %d\n", facesDescriptor[current.face][0]+current.y+1, facesDescriptor[current.face][1]+current.x+1, current.face+1)
	// 1000 * 53 + 4 * 81 + 0 = 53324

	return 1000*(facesDescriptor[current.face][0]+current.y+1) + 4*(facesDescriptor[current.face][1]+current.x+1) + ((current.face + 1) % 6)

}

func WaitKeyPress() {
	os.Stdin.Read(make([]byte, 1))
}

func SwitchFace(next Pos3D, outGoingdirection Direction, facing int, cube Cube) (Pos3D, int) {
	var newNext Pos3D
	var nextFacing int

	// var oldFace = next.face

	transition := transitions[next.face][facing]

	// switch to new face
	newNext.face = transition.face
	// fmt.Printf("Switching from Face %d to Face %d\n", next.face, newNext.face)

	switch transition.rotation {
	case 0:
		nextFacing = facing
		newNext.x = next.x
		newNext.y = next.y
	case 90:
		nextFacing = (facing + 1) % HEADINGS_SIZE
		switch outGoingdirection {
		case NORTH:
			newNext.x = 0
			newNext.y = next.x
		case SOUTH:
			newNext.x = cube.size - 1
			newNext.y = next.x
		case EAST:
			newNext.x = cube.size - 1 - next.y
			newNext.y = 0
		case WEST:
			newNext.x = cube.size - 1 - next.y
			newNext.y = cube.size - 1
		}
	case 180:
		nextFacing = (facing + 2) % HEADINGS_SIZE
		switch outGoingdirection {
		case NORTH:
			newNext.x = cube.size - 1 - next.x
			newNext.y = 0
		case SOUTH:
			newNext.x = cube.size - 1 - next.x
			newNext.y = cube.size - 1
		case EAST:
			newNext.x = cube.size - 1
			newNext.y = cube.size - 1 - next.y
		case WEST:
			newNext.x = 0
			newNext.y = cube.size - 1 - next.y
		}
	case -90:
		nextFacing = (facing - 1 + HEADINGS_SIZE) % HEADINGS_SIZE
		switch outGoingdirection {
		case NORTH:
			newNext.x = cube.size - 1
			newNext.y = cube.size - 1 - next.x
		case SOUTH:
			newNext.x = 0
			newNext.y = cube.size - 1 - next.x
		case EAST:
			newNext.x = next.y
			newNext.y = cube.size - 1
		case WEST:
			newNext.x = next.y
			newNext.y = 0
		}
	}

	// apply transition
	// fmt.Printf("new position: %+v\n", newNext)
	// fmt.Printf("heading: %c, new heading: %c\n", GetFacingAsChar(facing), GetFacingAsChar(nextFacing))

	return newNext, nextFacing
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

	var cube Cube
	// cube, moves = ParseInputPart2(4, facesDescriptor) // sample.txt - (startY, startX, startY+size, startX+size)

	// sample cube pattern
	//     0
	//   123
	//     45
	// sample transitions
	// transitions[0][NORTH_INDEX] = TransDestination{face: 1, rotation: 180} //   top,  south, 180
	// transitions[0][SOUTH_INDEX] = TransDestination{face: 3, rotation: 0}   //   top,  south,   0
	// transitions[0][EAST_INDEX] = TransDestination{face: 5, rotation: 180}  //  right,  west, 180
	// transitions[0][WEST_INDEX] = TransDestination{face: 2, rotation: -90}  //    top, south, -90
	// transitions[1][NORTH_INDEX] = TransDestination{face: 0, rotation: 180} //    top, south, 180
	// transitions[1][SOUTH_INDEX] = TransDestination{face: 4, rotation: 180} // bottom, north, 180
	// transitions[1][EAST_INDEX] = TransDestination{face: 2, rotation: 0}    //   left,  east,   0
	// transitions[1][WEST_INDEX] = TransDestination{face: 5, rotation: 90}   // bottom, north,  90
	// transitions[2][NORTH_INDEX] = TransDestination{face: 0, rotation: 90}  //   left, east,   90
	// transitions[2][SOUTH_INDEX] = TransDestination{face: 4, rotation: -90} //   left,  east, -90
	// transitions[2][EAST_INDEX] = TransDestination{face: 3, rotation: 0}    //   left, east,    0
	// transitions[2][WEST_INDEX] = TransDestination{face: 0, rotation: 0}    //  right, west,    0
	// transitions[3][NORTH_INDEX] = TransDestination{face: 0, rotation: 0}   // bottom, north,   0
	// transitions[3][SOUTH_INDEX] = TransDestination{face: 4, rotation: 0}   //    top, south,   0
	// transitions[3][EAST_INDEX] = TransDestination{face: 5, rotation: 90}   //    top, south,  90
	// transitions[3][WEST_INDEX] = TransDestination{face: 2, rotation: 0}    //  right, west,    0
	// transitions[4][NORTH_INDEX] = TransDestination{face: 3, rotation: 0}   // bottom, north,   0
	// transitions[4][SOUTH_INDEX] = TransDestination{face: 1, rotation: 180} // bottom, north, 180
	// transitions[4][EAST_INDEX] = TransDestination{face: 5, rotation: 0}    //   left, east,    0
	// transitions[4][WEST_INDEX] = TransDestination{face: 2, rotation: 90}   // bottom, north,  90
	// transitions[5][NORTH_INDEX] = TransDestination{face: 3, rotation: -90} //  right, west,  -90
	// transitions[5][SOUTH_INDEX] = TransDestination{face: 1, rotation: -90} //   left, east,  -90
	// transitions[5][EAST_INDEX] = TransDestination{face: 0, rotation: 180}  //  right, west,  180
	// transitions[5][WEST_INDEX] = TransDestination{face: 4, rotation: 0}    //  right, west,    0

	// var facesDescriptor [6][2]int = [6][2]int{{0, 8}, {4, 0}, {4, 4}, {4, 8}, {8, 8}, {8, 12}}
	// cube, moves = ParseInputPart2(4, facesDescriptor)

	// input cube pattern
	//    01
	//    2
	//   34
	//   5
	// input transitions
	transitions[0][NORTH_INDEX] = TransDestination{face: 5, rotation: 90}
	transitions[0][SOUTH_INDEX] = TransDestination{face: 2, rotation: 0}
	transitions[0][EAST_INDEX] = TransDestination{face: 1, rotation: 0}
	transitions[0][WEST_INDEX] = TransDestination{face: 3, rotation: 180}
	transitions[1][NORTH_INDEX] = TransDestination{face: 5, rotation: 0}
	transitions[1][SOUTH_INDEX] = TransDestination{face: 2, rotation: 90}
	transitions[1][EAST_INDEX] = TransDestination{face: 4, rotation: 180}
	transitions[1][WEST_INDEX] = TransDestination{face: 0, rotation: 0}
	transitions[2][NORTH_INDEX] = TransDestination{face: 0, rotation: 0}
	transitions[2][SOUTH_INDEX] = TransDestination{face: 4, rotation: 0}
	transitions[2][EAST_INDEX] = TransDestination{face: 1, rotation: -90}
	transitions[2][WEST_INDEX] = TransDestination{face: 3, rotation: -90}
	transitions[3][NORTH_INDEX] = TransDestination{face: 2, rotation: 90}
	transitions[3][SOUTH_INDEX] = TransDestination{face: 5, rotation: 0}
	transitions[3][EAST_INDEX] = TransDestination{face: 4, rotation: 0}
	transitions[3][WEST_INDEX] = TransDestination{face: 0, rotation: 180}
	transitions[4][NORTH_INDEX] = TransDestination{face: 2, rotation: 0}
	transitions[4][SOUTH_INDEX] = TransDestination{face: 5, rotation: 90}
	transitions[4][EAST_INDEX] = TransDestination{face: 1, rotation: 180}
	transitions[4][WEST_INDEX] = TransDestination{face: 3, rotation: 0}
	transitions[5][NORTH_INDEX] = TransDestination{face: 3, rotation: 0}
	transitions[5][SOUTH_INDEX] = TransDestination{face: 1, rotation: 0}
	transitions[5][EAST_INDEX] = TransDestination{face: 4, rotation: -90}
	transitions[5][WEST_INDEX] = TransDestination{face: 0, rotation: -90}

	var facesDescriptor [6][2]int = [6][2]int{{0, 50}, {0, 100}, {50, 50}, {100, 0}, {100, 50}, {150, 0}}
	cube, moves = ParseInputPart2(50, facesDescriptor)

	// cube.Print()
	// fmt.Println(moves)

	part2 := Part2(cube, moves, facesDescriptor) // 5031, 53324

	// cube.Print()

	return part1, part2
}
