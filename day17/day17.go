package main

import (
	_ "embed"
	"fmt"
)

//go:embed sample.txt
var input string

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

// const HEIGHT = 2_000_000_000_000
const HEIGHT = 1_000_000_000

type Board []byte

func NewBoard() (board Board) {
	board = make([]byte, HEIGHT)
	board[0] = 0b11111111
	//fmt.Println("memory allocation done")
	return board
}

func (board Board) Draw(upToHeight int) {
	for y := upToHeight; y >= 1; y-- {
		var line string
		for x := 0; x < 7; x++ {
			if board[y]&(1<<x) > 0 {
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
	draw    func(board Board, x int, y int) int
	hide    func(board Board, x int, y int)
	collide func(board Board, x int, y int, shiftX int, shiftY int) bool
}

var MinusShapeDraw = func(board Board, x int, y int) int {
	board[y] |= 0b00001111 << x
	return y
}

var MinusShapeHide = func(board Board, x int, y int) {
	board[y] &= ^(0b00001111 << x)
}

var MinusCollide = func(board Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	if x < 0 || x > 3 {
		return true
	}

	return board[y]&(0b00001111<<x) > 0
}

var CrossShapeDraw = func(board Board, x int, y int) int {
	board[y] |= 0b00000010 << x
	board[y+1] |= 0b00000111 << x
	board[y+2] |= 0b00000010 << x
	return y + 2
}

var CrossShapeHide = func(board Board, x int, y int) {
	board[y] &= ^(0b00000010 << x)
	board[y+1] &= ^(0b00000111 << x)
	board[y+2] &= ^(0b00000010 << x)
}

var CrossShapeCollide = func(board Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	if x < 0 || x > 4 {
		return true
	}

	return board[y]&(0b00000010<<x) > 0 || board[y+1]&(0b00000111<<x) > 0 || board[y+2]&(0b00000010<<x) > 0
}

var LShapeDraw = func(board Board, x int, y int) int {
	board[y] |= 0b00000111 << x
	board[y+1] |= 0b00000100 << x
	board[y+2] |= 0b00000100 << x
	return y + 2
}

var LShapeHide = func(board Board, x int, y int) {
	board[y] &= ^(0b00000111 << x)
	board[y+1] &= ^(0b00000100 << x)
	board[y+2] &= ^(0b00000100 << x)
}

var LShapeCollide = func(board Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	if x < 0 || x > 4 {
		return true
	}
	return board[y]&(0b00000111<<x) > 0 || board[y+1]&(0b00000100<<x) > 0 || board[y+2]&(0b00000100<<x) > 0
}

var IShapeDraw = func(board Board, x int, y int) int {
	board[y] |= 0b00000001 << x
	board[y+1] |= 0b00000001 << x
	board[y+2] |= 0b00000001 << x
	board[y+3] |= 0b00000001 << x
	return y + 3
}

var IShapeHide = func(board Board, x int, y int) {
	board[y] &= ^(0b00000001 << x)
	board[y+1] &= ^(0b00000001 << x)
	board[y+2] &= ^(0b00000001 << x)
	board[y+3] &= ^(0b00000001 << x)
}

var IShapeCollide = func(board Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	if x < 0 || x > 6 {
		return true
	}
	return board[y]&(0b00000001<<x) > 0 || board[y+1]&(0b00000001<<x) > 0 || board[y+2]&(0b00000001<<x) > 0 || board[y+3]&(0b00000001<<x) > 0
}

var SquareShapeDraw = func(board Board, x int, y int) int {
	board[y] |= 0b00000011 << x
	board[y+1] |= 0b00000011 << x
	return y + 1
}

var SquareShapeHide = func(board Board, x int, y int) {
	board[y] &= ^(0b00000011 << x)
	board[y+1] &= ^(0b00000011 << x)
}

var SquareShapeCollide = func(board Board, x int, y int, shiftX int, shiftY int) bool {
	x = x + shiftX
	y = y + shiftY
	if x < 0 || x > 5 {
		return true
	}
	return board[y]&(0b00000011<<x) > 0 || board[y+1]&(0b00000011<<x) > 0
}

var shapeCounter int = 0

var shapes = [5]Shape{
	{x: 0, y: 0, draw: MinusShapeDraw, collide: MinusCollide, hide: MinusShapeHide},
	{x: 0, y: 0, draw: CrossShapeDraw, collide: CrossShapeCollide, hide: CrossShapeHide},
	{x: 0, y: 0, draw: LShapeDraw, collide: LShapeCollide, hide: LShapeHide},
	{x: 0, y: 0, draw: IShapeDraw, collide: IShapeCollide, hide: IShapeHide},
	{x: 0, y: 0, draw: SquareShapeDraw, collide: SquareShapeCollide, hide: SquareShapeHide}}

func AppearNewShape(currentHeight int) (newShape *Shape) {
	newShape = &shapes[shapeCounter%5]
	newShape.x = 2
	newShape.y = currentHeight + 3
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

func DrawStep(board Board, currentShape *Shape, currentTime int, maxHeight int) {
	currentShape.draw(board, currentShape.x, currentShape.y)
	fmt.Println("time:", currentTime)
	board.Draw(maxHeight)
	currentShape.hide(board, currentShape.x, currentShape.y)
}

func PrintBoard(board Board) {

	for i := 0; i < HEIGHT; i++ {
		fmt.Printf("%c", board[i])
	}
	fmt.Println()

}

// var patternCounter int = 0
// var patternStart int = 0
// var patternStop int = 0
// var skipped int = 0

const N = 2022

// const N = 1_000_000_000_000

func Solve() (int, int) {
	var jet []int = ParseInput()
	var jetLen int = len(jet)

	var board Board = NewBoard()

	var currentTime int = 0
	var currentHeight int = 1

	var IsFalling bool = true
	var currentShape *Shape

	var lastXOfShapeWhenInSync int = 0
	var lastHeight int = 0
	var patternHeight int = 0
	var patternShapeCount int = 0
	var skippingPatternCount int = 0
	var lookingForPattern bool = true

	for shapeCounter < N {
		currentShape = AppearNewShape(currentHeight)
		shapeCounter++

		IsFalling = true

		for IsFalling {
			var jetShift int = jet[currentTime%jetLen]
			currentTime++

			if !currentShape.collide(board, currentShape.x, currentShape.y, jetShift, 0) {
				currentShape.x += jetShift
			}

			if !currentShape.collide(board, currentShape.x, currentShape.y, 0, -1) {
				currentShape.y--
			} else {
				IsFalling = false
				lastY := currentShape.draw(board, currentShape.x, currentShape.y)

				// if lookingForPattern && shapeCounter%5 == 0 && (currentTime-2)%jetLen == 0 {
				if lookingForPattern && shapeCounter%5 == 0 && (currentTime-2)%jetLen == 0 {

					if lastXOfShapeWhenInSync == currentShape.x {
						// synchronization point detected
						patternHeight = currentHeight - lastHeight
						patternShapeCount = shapeCounter - patternShapeCount

						fmt.Println("marker detected!:")
						fmt.Println("  current height:", currentHeight)
						fmt.Println("  pattern height:", patternHeight, "pattern shape count:", patternShapeCount, "shape count:", shapeCounter)
						remainingShapeToGenerateCount := (N - shapeCounter)
						skippingPatternCount = (remainingShapeToGenerateCount / patternShapeCount)
						stillToPlay := (remainingShapeToGenerateCount % patternShapeCount)
						fmt.Println("  we will skip ", skippingPatternCount, "patterns")
						shapeCounter = N - stillToPlay
						lookingForPattern = false

						// fmt.Println()
						// board.Draw(currentHeight + 6)
						// fmt.Println()

					} else {
						lastXOfShapeWhenInSync = currentShape.x
						lastHeight = currentHeight
						patternShapeCount = shapeCounter
					}
					//fmt.Println(currentHeight, shapeCounter%5, (currentTime-1)%jetLen, currentTime, currentShape.x)
				}

				currentHeight = max(lastY+1, currentHeight)
				// fmt.Println(currentHeight)
			}
		}
	}

	fmt.Println("skippingPatternCount:", skippingPatternCount, "patternHeight:", patternHeight)

	currentHeight += skippingPatternCount * patternHeight

	// fmt.Println()
	// board.Draw(currentHeight + 6)
	// board.Draw(320)
	// fmt.Println()

	part1 := currentHeight - 1 // 3068, 3071 / 1514285714288,

	part2 := 0
	return part1, part2
}
