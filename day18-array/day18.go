package main

import (
	"bufio"
	_ "embed"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

const size = 21

// func max(a int, b int) int {
// 	if a > b {
// 		return a
// 	}
// 	return b
// }

// func min(a int, b int) int {
// 	if a < b {
// 		return a
// 	}
// 	return b
// }

func ParseInput() *[size][size][size]byte {
	var scanArea [size][size][size]byte

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), ",")
		x, _ := strconv.Atoi(fields[0])
		y, _ := strconv.Atoi(fields[1])
		z, _ := strconv.Atoi(fields[2])

		scanArea[y][z][x] = 1
	}
	return &scanArea
}

func Part1(scanArea *[size][size][size]byte) int {
	visibleFaces := 0

	for y := 0; y < size; y++ {
		for z := 0; z < size; z++ {
			for x := 0; x < size; x++ {
				if scanArea[y][z][x] == 1 {
					if x+1 < size && scanArea[y][z][x+1] == 0 {
						visibleFaces++
					}
					if y+1 < size && scanArea[y+1][z][x] == 0 {
						visibleFaces++
					}
					if z+1 < size && scanArea[y][z+1][x] == 0 {
						visibleFaces++
					}
					if x-1 >= 0 && scanArea[y][z][x-1] == 0 {
						visibleFaces++
					}
					if y-1 >= 0 && scanArea[y-1][z][x] == 0 {
						visibleFaces++
					}
					if z-1 >= 0 && scanArea[y][z-1][x] == 0 {
						visibleFaces++
					}
				}
			}
		}
	}

	return visibleFaces

}

func flood(scanArea *[size][size][size]byte, startX int, startY int, startZ int) {
	if startX < 0 || startX >= size || startY < 0 || startY >= size || startZ < 0 || startZ >= size {
		return
	}

	if scanArea[startY][startZ][startX] > 0 {
		// either there is a cube, either we already visited that place, stop flooding
		return
	}

	// mark as visited
	scanArea[startY][startZ][startX] = 2

	// continue flooding
	flood(scanArea, startX+1, startY, startZ)
	flood(scanArea, startX, startY+1, startZ)
	flood(scanArea, startX, startY, startZ+1)
	flood(scanArea, startX-1, startY, startZ)
	flood(scanArea, startX, startY-1, startZ)
	flood(scanArea, startX, startY, startZ-1)
}

func Part2(scanArea *[size][size][size]byte) int {
	// var minX = math.MaxInt
	// var maxX = math.MinInt
	// var minY = math.MaxInt
	// var maxY = math.MinInt
	// var minZ = math.MaxInt
	// var maxZ = math.MinInt

	// for y := 0; y < size; y++ {
	// 	for z := 0; z < size; z++ {
	// 		for x := 0; x < size; x++ {
	// 			if scanArea[y][z][x] == 1 {
	// 				minX = min(x, minX)
	// 				maxX = max(x, maxX)
	// 				minY = min(y, minY)
	// 				maxY = max(y, maxY)
	// 				minZ = min(z, minZ)
	// 				maxZ = max(z, maxZ)
	// 			}
	// 		}
	// 	}
	// }

	// fmt.Println(minX, maxX, minY, maxY, minZ, maxZ)
	// flood(scanArea, maxX+1, maxY+1, maxZ+1)

	flood(scanArea, 20, 20, 20)

	exteriorFaces := 0

	for y := 0; y < size; y++ {
		for z := 0; z < size; z++ {
			for x := 0; x < size; x++ {
				if scanArea[y][z][x] == 1 {
					if x+1 >= size || scanArea[y][z][x+1] == 2 {
						exteriorFaces++
					}
					if y+1 >= size || scanArea[y+1][z][x] == 2 {
						exteriorFaces++
					}
					if z+1 >= size || scanArea[y][z+1][x] == 2 {
						exteriorFaces++
					}
					if x-1 < 0 || scanArea[y][z][x-1] == 2 {
						exteriorFaces++
					}
					if y-1 < 0 || scanArea[y-1][z][x] == 2 {
						exteriorFaces++
					}
					if z-1 < 0 || scanArea[y][z-1][x] == 2 {
						exteriorFaces++
					}
				}
			}
		}
	}
	return exteriorFaces
}

func Solve() (int, int) {
	var scanArea *[size][size][size]byte = ParseInput()
	part1 := Part1(scanArea) // 64, 3494
	part2 := Part2(scanArea) // 58, 2062
	return part1, part2
}
