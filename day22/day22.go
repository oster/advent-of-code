package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"strings"
)

//go:embed sample.txt
var input string

type Direction struct {
	yDirection int
	xDirection int
}

var NORTH = Direction{1, 0}
var EAST = Direction{0, 1}
var SOUTH = Direction{-1, 0}
var WEST = Direction{0, -1}

var HEADINGS [4]Direction = [4]Direction{NORTH, EAST, SOUTH, WEST}

type Move struct {
	length   int
	rotation int
}

func ParseInput() (data [][]byte, instructions []Move) {
	data = make([][]byte, 0)
	instructions = make([]Move, 0)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan(); len(scanner.Text()) > 1; scanner.Scan() {
		line := strings.TrimRight(scanner.Text(), "\n")
		var dataLine []byte = make([]byte, len(line))

		for idx := 0; idx < len(line); idx++ {
			char := line[idx]
			switch char {
			case ' ':
				dataLine[idx] = 0

			case '#', '.':
				dataLine[idx] = char

			default:
				panic("invalid character in puzzle map description" + fmt.Sprintf("[%c]", char))
			}
		}
		data = append(data, dataLine)
	}
	scanner.Scan()
	lastLine := scanner.Text()

	value := 0
	var move Move

	for idx := 0; idx < len(lastLine); idx++ {
		char := lastLine[idx]
		if char >= '0' && char <= '9' {
			value = value*10 + int(char-'0')
			continue
		} else {
			instructions = append(instructions, Move{length: value, rotation: 0})
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
		instructions = append(instructions, move)
	}

	if value != 0 {
		instructions = append(instructions, Move{length: value, rotation: 0})
	}
	return data, instructions
}

func PrintMap(data [][]byte) {
	for y := 0; y < len(data); y++ {
		for x := 0; x < len(data[y]); x++ {
			switch data[y][x] {
			case 0:
				fmt.Print(" ")
			case '#':
				fmt.Print("#")
			case '.':
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func Part1() int {
	return 0
}

func Part2() int {
	return 0
}

func Solve() (int, int) {
	var data [][]byte
	var instructions []Move

	data, instructions = ParseInput()

	PrintMap(data)
	fmt.Println()
	fmt.Println(instructions)

	data[0] = nil
	instructions[0] = Move{}
	part1 := 0
	part2 := 0
	return part1, part2
}
