package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

const WIDTH = 800
const HEIGHT = 180

func min(a int, b int) (int, int) {
	if a < b {
		return a, b
	} else {
		return b, a
	}
}

type Window struct {
	x1 int
	y1 int
	x2 int
	y2 int
}

func (current *Window) Update(newX int, newY int) {
	current.x1, _ = min(current.x1, newX)
	_, current.x2 = min(newX, current.x2)
	current.y1, _ = min(current.y1, newY)
	_, current.y2 = min(newY, current.y2)

}

func ParseInput(matrix *[HEIGHT][WIDTH]byte) Window {
	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	var window Window = Window{math.MaxInt, math.MaxInt, math.MinInt, math.MinInt}

	for scanner.Scan() {
		line := scanner.Text()
		var points []string = strings.Split(line, " -> ")

		coord := strings.Split(points[0], ",")
		currentX, _ := strconv.Atoi(coord[0])
		currentY, _ := strconv.Atoi(coord[1])

		window.Update(currentX, currentY)

		for i := 1; i < len(points); i++ {
			coord2 := strings.Split(points[i], ",")
			nextX, _ := strconv.Atoi(coord2[0])
			nextY, _ := strconv.Atoi(coord2[1])

			window.Update(nextX, nextY)

			startX, endX := min(currentX, nextX)
			for x := startX; x <= endX; x++ {
				matrix[currentY][x] = '#'
			}

			startY, endY := min(currentY, nextY)
			for y := startY; y <= endY; y++ {
				matrix[y][currentX] = '#'
			}

			currentX = nextX
			currentY = nextY
		}
	}

	matrix[0][500] = '+'

	return window
}

func PrintMatrix(matrix *[HEIGHT][WIDTH]byte, window Window) {
	for y := window.y1; y < window.y2+2; y++ {
		for x := window.x1; x < window.x2; x++ {
			if y == 0 && x == 500 {
				fmt.Print("+")
				continue
			}

			if matrix[y][x] == 0 {
				fmt.Print(".")
			} else {
				fmt.Printf("%c", matrix[y][x])
			}
		}
		fmt.Println()
	}
}

func FallSand(srcx int, srcy int, matrix *[HEIGHT][WIDTH]byte, floorY int, window *Window) int {
	step := 0
	generationFlag := true

	for generationFlag {
		step++

		sandx := srcx
		sandy := srcy + 1

		// filled up to source
		if matrix[sandy][sandx] == 'o' {
			generationFlag = false
			break
		}

		keepMoving := true

		for keepMoving {
			//window.Update(sandx+1, sandy+1)

			if sandy+1 == floorY {
				generationFlag = false // leaking, stop generation!
				break
			}

			if matrix[sandy+1][sandx] == 0 {
				sandy++
				continue
			}
			if matrix[sandy+1][sandx-1] == 0 {
				sandy++
				sandx--
				continue
			}
			if matrix[sandy+1][sandx+1] == 0 {
				sandx++
				sandy++
				continue
			}

			keepMoving = false
			break
		}
		matrix[sandy][sandx] = 'o'
	}

	return step - 1
}

func FallSand2(srcx int, srcy int, matrix *[HEIGHT][WIDTH]byte, floorY int, window *Window) int {
	step := 0
	generationFlag := true

	for generationFlag {
		step++

		sandx := srcx
		sandy := srcy

		// filled up to source
		if matrix[sandy][sandx] == 'o' {
			generationFlag = false
			break
		}

		keepMoving := true

		for keepMoving {
			//window.Update(sandx+1, sandy+1)

			if sandy+1 == floorY { // floor
				break
			}

			if matrix[sandy+1][sandx] == 0 {
				sandy++
				continue
			}
			if matrix[sandy+1][sandx-1] == 0 {
				sandy++
				sandx--
				continue
			}
			if matrix[sandy+1][sandx+1] == 0 {
				sandx++
				sandy++
				continue
			}

			keepMoving = false
			break
		}
		matrix[sandy][sandx] = 'o'
	}

	return step - 1
}

func Solve() (int, int) {
	var matrix [HEIGHT][WIDTH]byte
	var window Window = ParseInput(&matrix)

	fmt.Println(window)

	var matrixCopy [HEIGHT][WIDTH]byte
	for y := 0; y < HEIGHT; y++ {
		for x := 0; x < WIDTH; x++ {
			matrixCopy[y][x] = matrix[y][x]
		}
	}

	part1 := FallSand(500, 0, &matrix, HEIGHT, &window)
	// PrintMatrix(&matrix, Window{459, 13, 529, 170})
	part2 := FallSand2(500, 0, &matrixCopy, window.y2+2, &window)
	// PrintMatrix(&matrixCopy, Window{329, 0, 672, 172})

	return part1, part2 // 24 / 832, 140 / 27601
}
