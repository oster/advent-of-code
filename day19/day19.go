package main

import (
	"bufio"
	_ "embed"
	"fmt"
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

type State struct {
	ore      int
	clay     int
	obsidian int
	geode    int

	oreRobot      int
	clayRobot     int
	obsidianRobot int
	geodeRobot    int
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

var maxGeode int

func log(time int, state State, message string) {
	padding := ""
	for i := 0; i < time; i++ {
		padding += " "
	}
	fmt.Printf("%s %2d, [ore:%2d clay:%2d obsidian:%2d geode:%2d] [oreR:%2d clayR:%2d obsidianR:%2d geodeR:%2d]  %s\n", padding, time, state.ore, state.clay, state.obsidian, state.geode, state.oreRobot, state.clayRobot, state.obsidianRobot, state.geodeRobot, message)
}

func backtrackSearch(time int, state State, bp BluePrint, maxTime int, previousState State) {
	// log(time, state)
	if time > maxTime {
		// end of dedicated time
		return
	}

	newState := state

	newState.ore += state.oreRobot
	newState.clay += state.clayRobot
	newState.obsidian += state.obsidianRobot
	newState.geode += state.geodeRobot

	if newState.geode >= maxGeode {
		maxGeode = newState.geode
		// fmt.Println(maxGeode, "geode robot:", newState.geodeRobot)
		// fmt.Printf("%2d [ore:%2d clay:%2d obsidian:%2d geode:%2d] [oreR:%2d clayR:%2d obsidianR:%2d geodeR:%2d]\n", time, newState.ore, newState.clay, newState.obsidian, newState.geode, newState.oreRobot, newState.clayRobot, newState.obsidianRobot, newState.geodeRobot)
	}

	// for all actions
	if state.obsidian >= bp.geodeRobotCost.obsidian && state.ore >= bp.geodeRobotCost.ore {
		// buy a geode robot
		newState.geodeRobot++
		newState.obsidian -= bp.geodeRobotCost.obsidian
		newState.ore -= bp.geodeRobotCost.ore
		// log(time, newState, "bought a new GEODE robot")

		backtrackSearch(time+1, newState, bp, maxTime, state)
		newState.geodeRobot--
		newState.obsidian += bp.geodeRobotCost.obsidian
		newState.ore += bp.geodeRobotCost.ore
	}

	if state.clay >= bp.obsidianRobotCost.clay && state.ore >= bp.obsidianRobotCost.ore {
		if !(previousState.clay >= bp.obsidianRobotCost.clay && previousState.ore >= bp.obsidianRobotCost.ore && state.clay == previousState.clay && state.ore == previousState.ore) {
			// or, we could have bought it earlier... skip

			// buy an obsidian robot
			newState.obsidianRobot++
			newState.clay -= bp.obsidianRobotCost.clay
			newState.ore -= bp.obsidianRobotCost.ore
			//log(time, newState, "bought a new OBSIDIAN robot")

			backtrackSearch(time+1, newState, bp, maxTime, state)
			newState.obsidianRobot--
			newState.clay += bp.obsidianRobotCost.clay
			newState.ore += bp.obsidianRobotCost.ore
		}
	}

	if state.ore >= bp.clayRobotCost.ore {
		// if !(previousState.ore >= bp.clayRobotCost.ore && previousState.ore >= state.ore) {
		// or, we could have bought it earlier... skip

		// buy a clay robot
		newState.clayRobot++
		newState.ore -= bp.clayRobotCost.ore
		//log(time, newState, "bought a new CLAY robot")

		backtrackSearch(time+1, newState, bp, maxTime, state)
		newState.clayRobot--
		newState.ore += bp.clayRobotCost.ore
		// }
	}

	if state.ore >= bp.oreRobotCost.ore {
		// if !(previousState.ore >= bp.oreRobotCost.ore) {
		// or, we could have bought it earlier... skip

		// buy a ore robot
		newState.oreRobot++
		newState.ore -= bp.oreRobotCost.ore
		//log(time, newState, "bought a new ORE robot")

		backtrackSearch(time+1, newState, bp, maxTime, state)
		newState.oreRobot--
		newState.ore += bp.oreRobotCost.ore
		// }
	}

	if state.obsidian >= bp.geodeRobotCost.obsidian {
		// useless to not use them
		return
	}

	// if state.clay >= bp.obsidianRobotCost.clay {
	// 	// useless to not use them
	// 	return
	// }

	if state.ore >= bp.geodeRobotCost.ore && state.ore >= bp.obsidianRobotCost.ore && state.ore >= bp.clayRobotCost.ore && state.ore >= bp.oreRobotCost.ore {
		// useless to not use them
		return
	}

	backtrackSearch(time+1, newState, bp, maxTime, state)

}

func computeMaxForgeableGeodes(blueprint BluePrint, maxTime int) (maxGeodesCount int) {
	// fmt.Printf("%+v\n", blueprint)
	maxGeode = 0
	initialState := State{oreRobot: 1}
	backtrackSearch(1, initialState, blueprint, maxTime, initialState)

	maxGeodesCount = maxGeode
	// fmt.Println("max geode:", maxGeodesCount)

	return maxGeodesCount
}

func Part1(blueprints []BluePrint) (qualityLevel int) {
	var geodesPerBluePrint map[BluePrint]int = make(map[BluePrint]int)

	for i := 0; i < len(blueprints); i++ {
		x := computeMaxForgeableGeodes(blueprints[i], 24)
		fmt.Println(x)
		geodesPerBluePrint[blueprints[i]] = x
	}
	for bp, geodesCount := range geodesPerBluePrint {

		qualityLevel += bp.id * geodesCount
	}
	return qualityLevel
}

func Part2(blueprints []BluePrint) (number int) {
	number = 1

	size := 3
	if len(blueprints) < size {
		size = len(blueprints)
	}

	for i := 0; i < size; i++ {
		x := computeMaxForgeableGeodes(blueprints[i], 32)
		fmt.Println(x)
		number *= x
	}

	return number
}

var blueprints []BluePrint

func Solve() (int, int) {
	blueprints = ParseInput()

	// part1 := Part1(blueprints) // 33, 1177
	part1 := 0
	part2 := Part2(blueprints)
	// part2 := 0

	return part1, part2
}
