package main

import (
	_ "embed"
	"fmt"
)

//go:embed input.txt
var input string

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

const HEIGHT = 4000
const WIDTH = 9

type Board [HEIGHT][WIDTH]bool

func NewBoard() (board *Board) {
	board = &Board{}

	for y := 0; y < HEIGHT; y++ {
		board[y][0] = true
		board[y][WIDTH-1] = true
	}
	for x := 0; x < WIDTH; x++ {
		board[0][x] = true
	}

	return board
}

func (board *Board) Draw(upToHeight int) {
	for y := upToHeight; y >= 1; y-- {
		var line string
		for x := 1; x < WIDTH-1; x++ {
			if board[y][x] {
				line += "#"
			} else {
				line += "."
			}
		}

		fmt.Printf("|%v|\n", line)
	}
	fmt.Println("+-------+")

}

type Shape struct {
	x       int
	y       int
	draw    func(board *Board, x int, y int) int
	hide    func(board *Board, x int, y int)
	collide func(board *Board, x int, y int, shiftX int, shiftY int) bool
}

var MinusShapeDraw = func(board *Board, x int, y int) int {
	board[y][x] = true
	board[y][x+1] = true
	board[y][x+2] = true
	board[y][x+3] = true
	return y
}

var MinusShapeHide = func(board *Board, x int, y int) {
	board[y][x] = false
	board[y][x+1] = false
	board[y][x+2] = false
	board[y][x+3] = false
}

var MinusCollide = func(board *Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	return board[y][x] || board[y][x+1] || board[y][x+2] || board[y][x+3]
}

var CrossShapeDraw = func(board *Board, x int, y int) int {
	board[y][x+1] = true
	board[y+1][x] = true
	board[y+1][x+1] = true
	board[y+1][x+2] = true
	board[y+2][x+1] = true
	return y + 2
}

var CrossShapeHide = func(board *Board, x int, y int) {
	board[y][x+1] = false
	board[y+1][x] = false
	board[y+1][x+1] = false
	board[y+1][x+2] = false
	board[y+2][x+1] = false
}

var CrossShapeCollide = func(board *Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	return board[y][x+1] || board[y+1][x] || board[y+1][x+1] || board[y+1][x+2] || board[y+2][x+1]
}

var LShapeDraw = func(board *Board, x int, y int) int {
	board[y][x] = true
	board[y][x+1] = true
	board[y][x+2] = true
	board[y+1][x+2] = true
	board[y+2][x+2] = true
	return y + 2
}

var LShapeHide = func(board *Board, x int, y int) {
	board[y][x] = false
	board[y][x+1] = false
	board[y][x+2] = false
	board[y+1][x+2] = false
	board[y+2][x+2] = false
}

var LShapeCollide = func(board *Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	return board[y][x] || board[y][x+1] || board[y][x+2] || board[y+1][x+2] || board[y+2][x+2]
}

var IShapeDraw = func(board *Board, x int, y int) int {
	board[y][x] = true
	board[y+1][x] = true
	board[y+2][x] = true
	board[y+3][x] = true
	return y + 3
}

var IShapeHide = func(board *Board, x int, y int) {
	board[y][x] = false
	board[y+1][x] = false
	board[y+2][x] = false
	board[y+3][x] = false
}

var IShapeCollide = func(board *Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	return board[y][x] || board[y+1][x] || board[y+2][x] || board[y+3][x]
}

var SquareShapeDraw = func(board *Board, x int, y int) int {
	board[y][x] = true
	board[y][x+1] = true
	board[y+1][x] = true
	board[y+1][x+1] = true
	return y + 1
}

var SquareShapeHide = func(board *Board, x int, y int) {
	board[y][x] = false
	board[y][x+1] = false
	board[y+1][x] = false
	board[y+1][x+1] = false
}

var SquareShapeCollide = func(board *Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	return board[y][x] || board[y][x+1] || board[y+1][x] || board[y+1][x+1]
}

var shapeCounter int = 0

func AppearNewShape(currentHeight int) (newShape *Shape) {
	switch shapeCounter % 5 {
	case 0:
		newShape = &Shape{x: 3, y: currentHeight + 3, draw: MinusShapeDraw, collide: MinusCollide, hide: MinusShapeHide}
	case 1:
		newShape = &Shape{x: 3, y: currentHeight + 3, draw: CrossShapeDraw, collide: CrossShapeCollide, hide: CrossShapeHide}
	case 2:
		newShape = &Shape{x: 3, y: currentHeight + 3, draw: LShapeDraw, collide: LShapeCollide, hide: LShapeHide}
	case 3:
		newShape = &Shape{x: 3, y: currentHeight + 3, draw: IShapeDraw, collide: IShapeCollide, hide: IShapeHide}
	case 4:
		newShape = &Shape{x: 3, y: currentHeight + 3, draw: SquareShapeDraw, collide: SquareShapeCollide, hide: SquareShapeHide}
	}

	shapeCounter++
	return newShape
}

func ParseInput() (jet []int) {
	var size int = len(input) - 1 // skip '\n'
	jet = make([]int, size)

	for i := 0; i < size; i++ {
		if input[i] == '<' {
			jet[i] = -1
		} else {
			jet[i] = +1
		}
	}

	return jet
}

func DrawStep(board *Board, currentShape *Shape, currentTime int, maxHeight int) {
	currentShape.draw(board, currentShape.x, currentShape.y)
	fmt.Println("time:", currentTime)
	board.Draw(maxHeight)
	currentShape.hide(board, currentShape.x, currentShape.y)
}

const N = 2022

func Solve() (int, int) {

	var jet []int = ParseInput()
	var jetLen int = len(jet)

	var board *Board = NewBoard()

	var currentTime int = 0
	var currentHeight int = 1

	var jetShift int
	var IsFalling bool = true
	var currentShape *Shape

	for step := 0; step < N; step++ {
		currentShape = AppearNewShape(currentHeight)
		IsFalling = true

		for IsFalling {
			jetShift = jet[currentTime%jetLen]
			if !currentShape.collide(board, currentShape.x, currentShape.y, jetShift, 0) {
				currentShape.x += jetShift
			}

			if !currentShape.collide(board, currentShape.x, currentShape.y, 0, -1) {
				currentShape.y--
			} else {
				IsFalling = false
				currentHeight = max(currentShape.draw(board, currentShape.x, currentShape.y)+1, currentHeight)
			}
			currentTime++
		}
	}

	// fmt.Println()
	// fmt.Println()
	// board.Draw(currentHeight + 6)

	part1 := currentHeight - 1 // 3068, 3071 /
	part2 := 0
	return part1, part2
}
