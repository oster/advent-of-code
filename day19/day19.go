package main

import (
	"bufio"
	_ "embed"
	"strconv"
	"strings"
)

//go:embed sample.txt
var input string

type Cost struct {
	ore      int
	clay     int
	obsidian int
}

type BluePrint struct {
	id                int
	oreRobotCost      Cost
	clayRobotCost     Cost
	obsidianRobotCost Cost
	geodeRobotCost    Cost
}

func parseInt(field string) (result int) {
	result, _ = strconv.Atoi(field)
	return result
}

func ParseInput() (blueprints []BluePrint) {
	blueprints = make([]BluePrint, 0)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), " ")

		bp := BluePrint{id: parseInt(fields[1][:len(fields[1])-1]),
			oreRobotCost:      Cost{ore: parseInt(fields[6])},
			clayRobotCost:     Cost{ore: parseInt(fields[12])},
			obsidianRobotCost: Cost{ore: parseInt(fields[18]), clay: parseInt(fields[21])},
			geodeRobotCost:    Cost{ore: parseInt(fields[27]), obsidian: parseInt(fields[30])}}

		blueprints = append(blueprints, bp)
	}

	return blueprints
}

func Part1() int {
	return 0
}

func Part2() int {
	return 0
}

var blueprints []BluePrint

func Solve() (int, int) {
	blueprints = ParseInput()

	part1 := 0
	part2 := 0
	return part1, part2
}
