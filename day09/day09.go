package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

type Move struct {
	direction byte
	length    int
}

type Point struct {
	x int
	y int
}

const SIZE = 10

func parseData(data string) []Move {
	var log []Move = make([]Move, 0)

	scanner := bufio.NewScanner(strings.NewReader(data))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		line := strings.Split(strings.TrimRight(scanner.Text(), "\n\r"), " ")

		move := Move{}
		move.direction = line[0][0]
		move.length, _ = strconv.Atoi(line[1])

		log = append(log, move)
	}

	return log
}

func DisplayMatrice(size int, h Point, t Point, s Point) {
	for y := size; y >= -size; y-- {
		for x := -size; x <= size; x++ {
			if x == s.x && y == s.y {
				fmt.Print("s")
				continue
			}
			if x == h.x && y == h.y {
				fmt.Print("H")
				continue
			}
			if x == t.x && y == t.y {
				fmt.Print("T")
				continue
			}
			fmt.Print(".")

		}
		fmt.Println()
	}
	fmt.Println()
}

func DisplaySnakeMatrice(size int, snake [10]Point, s Point) {
	for y := size; y >= -size; y-- {
		for x := -size; x <= size; x++ {

			found := false
		out:
			for idx, p := range snake {
				if x == p.x && y == p.y {
					if idx == 0 {
						found = true
						fmt.Print("H")
						break out
					}
					found = true
					fmt.Print(idx)
					break out
				}
			}
			if !found {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
	fmt.Println()
}

func DisplayAllPointsMatrice(size int, ts []Point) {
	for y := size; y >= -size; y-- {
		for x := -size; x <= size; x++ {
			if x == 0 && y == 0 {
				fmt.Print("s")
				continue
			}
			found := false
			for _, t := range ts {
				if x == t.x && y == t.y {
					fmt.Print("#")
					found = true
					break
				}
			}
			if !found {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func MoveOneStep(h Point, move Move) Point {
	switch move.direction {
	case 'R':
		h.x += 1
	case 'L':
		h.x -= 1
	case 'U':
		h.y += 1
	case 'D':
		h.y -= 1
	}
	return h
}

func Follow(h Point, t Point) Point {
	dx := h.x - t.x
	dy := h.y - t.y

	if (dx == 1 || dx == 0 || dx == -1) && (dy == 1 || dy == 0 || dy == -1) {
		return t
	}

	// abs(dx) > 1 || abs(dy) > 1
	if dy > 0 {
		t.y += 1
	} else if dy < 0 {
		t.y -= 1
	}

	if dx > 0 {
		t.x += 1
	} else if dx < 0 {
		t.x -= 1
	}

	return t
}

func ReplayPart1(log []Move) []Point {
	var result []Point = make([]Point, 0)
	result = append(result, Point{0, 0})
	h := Point{0, 0}
	t := Point{0, 0}

	for _, move := range log {
		for i := 0; i < move.length; i++ {
			h = MoveOneStep(h, move)
			t = Follow(h, t)
			//DisplayMatrice(10, h, t, Point{0, 0})

			result = append(result, Point{t.x, t.y})
		}
	}

	result = RemoveDuplicate(result)
	//DisplayAllPointsMatrice(10, result)

	return result
}

func ReplayPart2(log []Move) []Point {
	var result []Point = make([]Point, 0)
	result = append(result, Point{0, 0})

	snake := [10]Point{}

	for _, move := range log {
		for i := 0; i < move.length; i++ {
			// m = move
			snake[0] = MoveOneStep(snake[0], move)
			for k := 1; k < len(snake); k++ {
				snake[k] = Follow(snake[k-1], snake[k])

			}
			//DisplaySnakeMatrice(10, snake, Point{0, 0})
			result = append(result, Point{snake[9].x, snake[9].y})
		}
		//DisplaySnakeMatrice(10, snake, Point{0, 0})
	}

	result = RemoveDuplicate(result)
	//DisplayAllPointsMatrice(10, result)

	return result
}

func RemoveDuplicate(list []Point) []Point {
	for i := 0; i < len(list); i++ {
		for j := i + 1; j < len(list); j++ {
			if list[i].x == list[j].x && list[i].y == list[j].y {
				list = append(list[:j], list[j+1:]...)
				j--
			}
		}
	}
	return list
}

func Solve() (int, int) {
	log := parseData(input)
	part1 := len(ReplayPart1(log))
	part2 := len(ReplayPart2(log))
	return part1, part2 // 13/6190, 32/2516
}
