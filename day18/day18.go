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
	var scanAres Cubes = Cubes{}

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), ",")
		x, _ := strconv.Atoi(fields[0])
		y, _ := strconv.Atoi(fields[1])
		z, _ := strconv.Atoi(fields[2])

		scanAres[Cube{x, y, z}] = true
	}
	return scanAres
}

func Part1(scanAres Cubes) int {
	visibleFaces := 0

	for cube := range scanAres {
		if _, ok := scanAres[Cube{cube.x + 1, cube.y, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanAres[Cube{cube.x, cube.y + 1, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanAres[Cube{cube.x, cube.y, cube.z + 1}]; !ok {
			visibleFaces++
		}
		if _, ok := scanAres[Cube{cube.x - 1, cube.y, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanAres[Cube{cube.x, cube.y - 1, cube.z}]; !ok {
			visibleFaces++
		}
		if _, ok := scanAres[Cube{cube.x, cube.y, cube.z - 1}]; !ok {
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

func flood(scanAres Cubes, startX int, startY int, startZ int) {
	if startX < minX-1 || startX > maxX+1 || startY < minY-1 || startY > maxY+1 || startZ < minZ-1 || startZ > maxZ+1 {
		return
	}

	if _, ok := scanAres[Cube{startX, startY, startZ}]; ok {
		// either there is a cube, either we already visited that place, stop flooding
		return
	}

	// mark as visited
	scanAres[Cube{startX, startY, startZ}] = false

	// continue flooding
	flood(scanAres, startX+1, startY, startZ)
	flood(scanAres, startX, startY+1, startZ)
	flood(scanAres, startX, startY, startZ+1)
	flood(scanAres, startX-1, startY, startZ)
	flood(scanAres, startX, startY-1, startZ)
	flood(scanAres, startX, startY, startZ-1)
}

func Part2(scanAres Cubes) int {
	for cube := range scanAres {
		minX = min(cube.x, minX)
		maxX = max(cube.x, maxX)
		minY = min(cube.y, minY)
		maxY = max(cube.y, maxY)
		minZ = min(cube.z, minZ)
		maxZ = max(cube.z, maxZ)
	}

	flood(scanAres, maxX+1, maxY+1, maxZ+1)

	exteriorFaces := 0
	for cube, isCube := range scanAres {
		if !isCube {
			continue
		}

		if val, ok := scanAres[Cube{cube.x + 1, cube.y, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanAres[Cube{cube.x, cube.y + 1, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanAres[Cube{cube.x, cube.y, cube.z + 1}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanAres[Cube{cube.x - 1, cube.y, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanAres[Cube{cube.x, cube.y - 1, cube.z}]; ok && !val {
			exteriorFaces++
		}
		if val, ok := scanAres[Cube{cube.x, cube.y, cube.z - 1}]; ok && !val {
			exteriorFaces++
		}
	}
	return exteriorFaces
}

func Solve() (int, int) {
	var scanAres Cubes = ParseInput()
	part1 := Part1(scanAres) // 64, 3494
	part2 := Part2(scanAres) // 58, 2062
	return part1, part2
}
