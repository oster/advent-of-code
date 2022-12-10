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

const SCREEN_WIDTH = 40
const SCREEN_HEIGHT = 6

var screen [SCREEN_HEIGHT][SCREEN_WIDTH]bool

var cycle int = 0
var register int = 1
var sumOfSignalStrength int = 0

func UpdateSignalStrength() {
	if (cycle-20)%40 == 0 {
		sumOfSignalStrength += register * cycle
	}
}

func PrintScreen() {
	var scr string
	for row := 0; row < SCREEN_HEIGHT; row++ {
		for col := 0; col < SCREEN_WIDTH; col++ {
			if screen[row][col] {
				scr += "█"
			} else {
				scr += "."
			}
		}
		scr += "\n"
	}
	fmt.Println(scr)
}

var row int = 0

func Crt() {
	synced := cycle % SCREEN_WIDTH
	if synced == register-1 || synced == register || synced == register+1 {
		screen[row][synced] = true
	}

	if (cycle+1)%SCREEN_WIDTH == 0 {
		row++
	}
}

func Part1() int {
	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	Crt()
	for scanner.Scan() {
		line := scanner.Text()

		// noop or 1st cycle of addx
		cycle++
		UpdateSignalStrength()
		Crt()

		if line[0] == 'a' { // 2nd cycle of addx
			cycle++
			UpdateSignalStrength()
			value, _ := strconv.Atoi(line[5:])
			register += value
			Crt()
		}
	}

	return sumOfSignalStrength
}

func Solve() (int, int) {
	part1 := Part1()
	PrintScreen()

	part2 := 0
	return part1, part2 // 13140/17020 , / RLEZFLGE
}
