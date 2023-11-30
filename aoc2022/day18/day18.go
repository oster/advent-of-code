package main

import (
	"bufio"
	_ "embed"
	"math"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

type Cube struct {
	x int
	y int
	z int
}

type Cubes map[Cube]bool

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func ParseInput() Cubes {
	var scanarea Cubes = Cubes{}

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), ",")
		x, _ := strconv.Atoi(fields[0])
		y, _ := strconv.Atoi(fields[1])
		z, _ := strconv.Atoi(fields[2])

		scanarea[Cube{x, y, z}] = true
	}
	return scanarea
}

func Part1(scanarea Cubes) int {
	visibleFaces := 0

	for cube := range scanarea {
		if _, ok := scanarea[Cube{cube.x + 1, cube.y, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanarea[Cube{cube.x, cube.y + 1, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanarea[Cube{cube.x, cube.y, cube.z + 1}]; !ok {
			visibleFaces++
		}
		if _, ok := scanarea[Cube{cube.x - 1, cube.y, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanarea[Cube{cube.x, cube.y - 1, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanarea[Cube{cube.x, cube.y, cube.z - 1}]; !ok {
			visibleFaces++
		}
	}
	return visibleFaces

}

var minX = math.MaxInt
var maxX = math.MinInt
var minY = math.MaxInt
var maxY = math.MinInt
var minZ = math.MaxInt
var maxZ = math.MinInt

func flood(scanarea Cubes, startX int, startY int, startZ int) {
	if startX < minX-1 || startX > maxX+1 || startY < minY-1 || startY > maxY+1 || startZ < minZ-1 || startZ > maxZ+1 {
		return
	}

	if _, ok := scanarea[Cube{startX, startY, startZ}]; ok {
		// either there is a cube, either we already visited that place, stop flooding
		return
	}

	// mark as visited
	scanarea[Cube{startX, startY, startZ}] = false

	// continue flooding
	flood(scanarea, startX+1, startY, startZ)
	flood(scanarea, startX, startY+1, startZ)
	flood(scanarea, startX, startY, startZ+1)
	flood(scanarea, startX-1, startY, startZ)
	flood(scanarea, startX, startY-1, startZ)
	flood(scanarea, startX, startY, startZ-1)
}

func Part2(scanarea Cubes) int {
	for cube := range scanarea {
		minX = min(cube.x, minX)
		maxX = max(cube.x, maxX)
		minY = min(cube.y, minY)
		maxY = max(cube.y, maxY)
		minZ = min(cube.z, minZ)
		maxZ = max(cube.z, maxZ)
	}

	flood(scanarea, maxX+1, maxY+1, maxZ+1)

	exteriorFaces := 0
	for cube, isCube := range scanarea {
		if !isCube {
			continue
		}

		if val, ok := scanarea[Cube{cube.x + 1, cube.y, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanarea[Cube{cube.x, cube.y + 1, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanarea[Cube{cube.x, cube.y, cube.z + 1}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanarea[Cube{cube.x - 1, cube.y, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanarea[Cube{cube.x, cube.y - 1, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanarea[Cube{cube.x, cube.y, cube.z - 1}]; ok && !val {
			exteriorFaces++
		}
	}
	return exteriorFaces
}

func Solve() (int, int) {
	var scanarea Cubes = ParseInput()
	part1 := Part1(scanarea) // 64, 3494
	part2 := Part2(scanarea) // 58, 2062
	return part1, part2
}
