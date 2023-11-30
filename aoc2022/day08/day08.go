package main

import (
	"bufio"
	_ "embed"
	"strings"
)

//go:embed input.txt
var input string

const N = 99

func parseData(data string) [N][N]byte {
	var heights [N][N]byte

	scanner := bufio.NewScanner(strings.NewReader(data))
	scanner.Split(bufio.ScanLines)
	j := 0
	for scanner.Scan() {
		line := strings.TrimRight(scanner.Text(), "\n\r")
		for i, c := range line {
			heights[j][i] = byte(c) - '0'
		}
		j++
	}

	return heights
}

func ComputeVisibility(heights [N][N]byte) [N][N]bool {
	const n = len(heights[0])
	var visibility [N][N]bool

	// trees at borders are always visible
	for i := 0; i < n; i++ {
		visibility[i][0] = true
		visibility[i][n-1] = true
		visibility[0][i] = true
		visibility[n-1][i] = true
	}

	for i := 1; i < n-1; i++ {
		maxG := heights[i][0]
		for j := 1; j < n-1; j++ {
			if heights[i][j] > maxG {
				visibility[i][j] = true
				maxG = heights[i][j]
			}
		}

		maxD := heights[i][n-1]
		for j := n - 2; j > 0; j-- {
			if heights[i][j] > maxD {
				visibility[i][j] = true
				maxD = heights[i][j]
			}
		}
	}

	for i := 1; i < n-1; i++ {
		maxT := heights[0][i]
		for j := 1; j < n-1; j++ {
			if heights[j][i] > maxT {
				visibility[j][i] = true
				maxT = heights[j][i]
			}
		}

		maxB := heights[n-1][i]
		for j := n - 2; j > 0; j-- {
			if heights[j][i] > maxB {
				visibility[j][i] = true
				maxB = heights[j][i]
			}
		}
	}

	return visibility
}

func ComputeVisibleTrees(visibility [N][N]bool) int {
	const n = len(visibility[0])
	count := 0
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if visibility[i][j] {
				count++
			}
		}
	}

	return count
}

func ComputeScenicScore(heights [N][N]byte, visibilities [N][N]bool) int {
	const n = len(visibilities[0])
	maxScenicScore := 0

	for i := 1; i < n-1; i++ {
		for j := 1; j < n-1; j++ {
			// we only consider visible tree for placing the house
			if !visibilities[i][j] {
				continue
			}

			scenicScore := 1
			houseHeight := heights[i][j]

			// we consider all directions (north, south, east, west)
			// SLOWER ;(
			// for _, steps := range [][2]int{{-1, 0}, {1, 0}, {0, 1}, {0, -1}} {
			// 	distance := 0

			// 	k := i + steps[0]
			// 	l := j + steps[1]

			// 	for k >= 0 && k < n && l >= 0 && l < n {
			// 		distance++

			// 		if heights[k][l] >= houseHeight {
			// 			break
			// 		}
			// 		k += steps[0]
			// 		l += steps[1]
			// 	}
			// 	scenicScore *= distance
			// }

			// looking at north
			distance := 0
			for k := i - 1; k >= 0; k-- {
				distance++
				if heights[k][j] >= houseHeight {
					break
				}
			}
			scenicScore *= distance

			// looking at south
			distance = 0
			for k := i + 1; k < n; k++ {
				distance++
				if heights[k][j] >= houseHeight {
					break
				}
			}
			scenicScore *= distance

			// looking at east
			distance = 0
			for k := j + 1; k < n; k++ {
				distance++
				if heights[i][k] >= houseHeight {
					break
				}
			}
			scenicScore *= distance

			// looking at west
			distance = 0
			for k := j - 1; k >= 0; k-- {
				distance++
				if heights[i][k] >= houseHeight {
					break
				}
			}
			scenicScore *= distance

			if scenicScore > maxScenicScore {
				maxScenicScore = scenicScore
			}
		}
	}

	return maxScenicScore
}

func Solve() (int, int) {
	heights := parseData(input)
	visibilities := ComputeVisibility(heights)
	scenicScore := ComputeScenicScore(heights, visibilities)

	return ComputeVisibleTrees(visibilities), scenicScore // 21/1796, 8/288120
}
