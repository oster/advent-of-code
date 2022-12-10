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

func computeSignal(cycle int, register int) int {
	signalStrength := 0

	signalStrength = register * cycle
	// fmt.Println("cycle: ", cycle, "register: ", register, "\tsignal strength : ", signalStrength)

	return signalStrength
}

var screen [6][40]bool

func printScreen() {
	for _, line := range screen {
		for _, pixel := range line {
			if pixel {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

var y int

func Crt(cycle int, register int) {
	// fmt.Println(register)

	//fmt.Println(cycle, "y:", y)
	sync := cycle % 40
	if sync == register-1 || sync == register || sync == register+1 {
		// screen[y][sync] = screen[y][sync] || true
		screen[y][sync] = true
	}

	if (cycle+1)%40 == 0 {
		y = (y + 1) % 7
	}
}

func Part1() int {
	instructionCounter := 0

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	cycle := 0
	register := 1

	signalStrength := 0
	sumOfSignalStrength := 0

	Crt(cycle, register)

	for scanner.Scan() {
		line := strings.TrimRight(scanner.Text(), "\n\r")

		cycle++
		instructionCounter++

		if cycle == 20 || (cycle-20)%40 == 0 {
			signalStrength = computeSignal(cycle, register)
			sumOfSignalStrength += signalStrength
		}

		Crt(cycle, register)

		if line[0] == 'n' { // noop
			// skip
		} else if line[0] == 'a' { // addx
			value, _ := strconv.Atoi(line[5:])

			cycle++

			if cycle == 20 || (cycle-20)%40 == 0 {
				signalStrength = computeSignal(cycle, register)
				sumOfSignalStrength += signalStrength
			}
			register += value

			Crt(cycle, register)

		}

	}

	// fmt.Print("instruction counter: ", instructionCounter, "\t")
	// fmt.Println("cycle: ", cycle, " register: ", register)

	return sumOfSignalStrength

}

func Solve() (int, int) {
	part1 := Part1()

	printScreen()
	part2 := 0
	return part1, part2 // 13140/17020 , / RLEZFLGE
}
