package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"

	"github.com/edwingeng/deque/v2"
)

//go:embed input.txt
var input string

const N = 59 // 10 //59

func min(a int, b int) (int, int) {
	if a < b {
		return a, b
	} else {
		return b, a
	}
}

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func Contains(values []string, val string) bool {
	for i := 0; i < len(values); i++ {
		if values[i] == val {
			return true
		}
	}
	return false
}

func PathContains(path []int, val int) bool {
	for i := 0; i < len(path); i++ {
		if path[i] == val {
			return true
		}
	}
	return false
}

type Valve struct {
	id            string
	flow          int
	connectedWith []string
}

var valves []Valve = make([]Valve, 0)

func PrintDistances(distances *[N][N]int) {
	for idxSrc, valveSrc := range valves {
		fmt.Println("From Valve", valveSrc.id)
		for idxDst, valveDst := range valves {
			fmt.Println("   to Valve", valveDst.id, "=", distances[idxSrc][idxDst])
		}
	}
}

func PrintMatrix(value *[N][N]int) {
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			fmt.Print(value[i][j], " ")
		}
		fmt.Println()
	}
}

func CopyMatrix(m *[N][N]int) *[N][N]int {
	var copy [N][N]int

	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			copy[i][j] = m[i][j]
		}
	}

	return &copy
}

func MultMatrix(m *[N][N]int, n *[N][N]int) *[N][N]int {
	var res [N][N]int

	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			cij := 0
			for k := 0; k < N; k++ {
				cij += m[i][k] * n[k][j]
			}
			res[i][j] = cij
		}
	}
	return &res
}

func ComputeAdjacencyMatrix() *[N][N]int {
	var res [N][N]int

	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			if Contains(valves[i].connectedWith, valves[j].id) {
				res[i][j] = 1
			}
		}
	}

	return &res
}

func MergeMatrix(d *[N][N]int, x *[N][N]int, exp int) bool {
	res := true

	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			if d[i][j] == 0 && x[i][j] > 0 {
				d[i][j] = exp
				res = false
			}
		}
	}

	return res
}

func ComputeDistancesMatrix() *[N][N]int {
	var adj *[N][N]int = ComputeAdjacencyMatrix()
	var distances *[N][N]int = CopyMatrix(adj)

	expMatrix := CopyMatrix(adj)
	exp := 1
	for {
		exp++
		expMatrix = MultMatrix(expMatrix, adj)
		if MergeMatrix(distances, expMatrix, exp) {
			break
		}
	}
	for i := 0; i < N; i++ {
		distances[i][i] = 0
	}
	return distances
}

type State struct {
	t           int
	location    int
	valveStates [N]bool
	production  int
}

func GetInstantPressure(state *State) int {
	pressure := 0
	for i := 0; i < N; i++ {
		if state.valveStates[i] {
			pressure += valves[i].flow
		}
	}
	return pressure
}

func PrintReportState(state *State) {
	fmt.Println("== Minute", state.t, "==")

	openedValvesCount := 0
	for idx, v := range valves {
		if state.valveStates[idx] {
			openedValvesCount++
			fmt.Print("valve ", v.id, " is open, ")
		}
	}
	if openedValvesCount == 0 {
		fmt.Println("No valves are open.")
	} else {
		fmt.Println("releasing", GetInstantPressure(state), "pressure")
	}

}

func UpdateProduction(state *State, kTimes int) {
	for i := 0; i < N; i++ {
		if state.valveStates[i] {
			state.production += kTimes * valves[i].flow
		}
	}
}

func ParseInput() {
	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	var name string
	var flow int

	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), " ")

		name = fields[1]
		flow, _ = strconv.Atoi(fields[4][5 : len(fields[4])-1])

		var connectedTo []string = make([]string, 0)
		for i := 9; i < len(fields); i++ {
			connectedTo = append(connectedTo, strings.TrimRight(fields[i][:len(fields[i])], ","))
		}

		v := Valve{name, flow, connectedTo}
		valves = append(valves, v)

		// so "AA" is always the first valve at index 0
		sort.SliceStable(valves, func(i int, j int) bool {
			return valves[i].id < valves[j].id
		})
	}
}

func Part1(maxTime int, distances *[N][N]int) int {
	var valvesIndexes []int = GetIndexesOfValvesWithPositivePressure()
	return Part1_BFS(maxTime, distances, valvesIndexes)
}

func Part1_BFS(maxTime int, distances *[N][N]int, valvesIndexes []int) int {
	var currentState = State{t: 1, location: 0, production: 0}
	states := deque.NewDeque[State]()

	states.PushBack(currentState)

	var visitedState map[State]bool = make(map[State]bool)

	maxProd := 0

	for !states.IsEmpty() {
		currentState = states.PopFront()

		if currentState.production > maxProd {
			maxProd = currentState.production
		}

		// action = all moves to usefull valves
		for _, idxValve := range valvesIndexes {
			if idxValve == currentState.location {
				// we do not move
				// action = open the vanne
				if !currentState.valveStates[currentState.location] && valves[currentState.location].flow > 0 {
					newState := currentState
					newState.t += 1
					newState.valveStates[currentState.location] = true
					UpdateProduction(&newState, 1)

					// we "memoize" this new state
					if newState.t <= maxTime {
						// PrintReportState(&currentState)
						// fmt.Println("You open valve", valves[currentState.location].id)
						_, ok := visitedState[newState]
						if !ok {
							visitedState[newState] = true
							states.PushBack(newState)
						}
					}
				}

				continue
			}

			if valves[idxValve].flow == 0 {
				// skip if vanne does not free any pressure
				continue
			}
			if currentState.valveStates[idxValve] {
				// skip if vannes is already opened
				continue
			}
			if currentState.t+distances[currentState.location][idxValve] > maxTime {
				// skip if out of time
				continue
			}

			newState := currentState
			newState.location = idxValve
			newState.t += distances[currentState.location][idxValve]
			UpdateProduction(&newState, distances[currentState.location][idxValve])

			// we "memoize" this new state
			if newState.t <= maxTime {
				_, ok := visitedState[newState]
				if !ok {
					// PrintReportState(&currentState)
					// fmt.Println("You move to valve", valves[newState.location].id)
					visitedState[newState] = true
					states.PushBack(newState)
				}
			}
		}

		// action = wait till the end
		newState := currentState
		jump := maxTime - newState.t
		newState.t = maxTime
		UpdateProduction(&newState, jump)

		_, ok := visitedState[newState]
		if !ok {
			// PrintReportState(&currentState)
			//fmt.Println("waiting.")
			visitedState[newState] = true
			states.PushBack(newState)
		}
	}

	return maxProd
}

func GetIndexesOfValvesWithPositivePressure() []int {
	var useFullValvesIndex []int = make([]int, 0)
	for idx, v := range valves {
		if v.flow > 0 {
			useFullValvesIndex = append(useFullValvesIndex, idx)
		}
	}

	return useFullValvesIndex
}

var bestGain int = 0
var bestPath []int

func Part1_Backtracking(startValveIndex int, distances *[N][N]int) (int, []int) {
	var valvesIndex []int = GetIndexesOfValvesWithPositivePressure()
	bestGain = 0
	bestPath = nil
	var taken []bool = make([]bool, len(valvesIndex))
	Part1_Backtracking_Solver(30, valvesIndex, []int{startValveIndex}, distances, 0, 0, 0, taken)
	return bestGain, bestPath
}

func Part1_Backtracking_Solver(timeLimit int, valvesIndex []int, path []int, distances *[N][N]int, depth int, cost int, gain int, taken []bool) {
	if depth > len(valvesIndex) {
		return
	}

	if gain > bestGain {
		bestGain = gain
		bestPath = make([]int, len(path))
		copy(bestPath, path)
	}

	for i := 0; i < len(valvesIndex); i++ {
		if taken[i] {
			continue
		}
		taken[i] = true
		path = append(path, valvesIndex[i])

		t := distances[path[depth]][valvesIndex[i]] + 1
		if cost+t < timeLimit {
			newGain := gain + (timeLimit-(cost+t))*valves[valvesIndex[i]].flow
			Part1_Backtracking_Solver(timeLimit, valvesIndex, path, distances, depth+1, cost+t, newGain, taken)
		}

		taken[i] = false
		path = path[:depth+1]
	}
}

func ComputeCostAndGainOfPath(maxTime int, distances *[N][N]int, p []int) (cost int, gain int) {
	for i := 1; i < len(p); i++ {
		t := distances[p[i-1]][p[i]] + 1
		cost += t
		gain += (maxTime - cost) * valves[p[i]].flow
	}
	return cost, gain
}

func SelectValvesFromBitString(valvesIndexes []int, valvesBitString int) (selectedValvesIndexes []int) {
	selectedValvesIndexes = make([]int, 0)

	index := 0
	for valvesBitString > 0 {
		if valvesBitString&1 > 0 {
			selectedValvesIndexes = append(selectedValvesIndexes, valvesIndexes[index])
		}
		valvesBitString = valvesBitString >> 1
		index++
	}

	return selectedValvesIndexes
}

func Part2_Split(timeLimit int, startValveIndex int, distances *[N][N]int) (totalGain int) {
	var valvesIndexes []int = GetIndexesOfValvesWithPositivePressure()
	// var manPath, elephantPath []int

	totalGain = math.MinInt
	valvesCount := len(valvesIndexes)
	valvesBitString := (1 << valvesCount) - 1 // all bits at 1 == all valves

	var gains map[int]int = make(map[int]int)     // valves bitstring -> bestgain
	var paths map[int][]int = make(map[int][]int) // valves bitstring -> best path (valves indexes)

	for selection := 0; selection < (valvesBitString + 1); selection++ {
		// fmt.Printf("%05b %05b\n", selection, remaining)
		var selectedValvesIndexes []int = SelectValvesFromBitString(valvesIndexes, selection)
		remaining := valvesBitString ^ selection

		if _, known := gains[selection]; !known {
			bestGain = 0
			bestPath = nil
			var taken []bool = make([]bool, len(selectedValvesIndexes))
			Part1_Backtracking_Solver(timeLimit, selectedValvesIndexes, []int{startValveIndex}, distances, 0, 0, 0, taken)

			// bestGain = Part1_BFS(timeLimit, distances, selectedValvesIndexes)
			gains[selection] = bestGain
			paths[selection] = bestPath
		}

		// fmt.Printf("%d %016b %v\n", gains[selection], selection, paths[selection])
		// fmt.Printf("%d %016b %v\n", gains[remaining], remaining, paths[remaining])

		// totalGain = max(totalGain, gains[selection]+gains[remaining])
		if gains[selection]+gains[remaining] > totalGain {
			totalGain = gains[selection] + gains[remaining]
			// manPath = paths[selection]
			// elephantPath = paths[remaining]
		}
	}

	// fmt.Println(totalGain)
	// cost, gain := ComputeCostAndGainOfPath(timeLimit, distances, manPath)
	// fmt.Printf("man path: %v, cost:%d gain:%d\n", manPath, cost, gain)

	// cost, gain = ComputeCostAndGainOfPath(timeLimit, distances, elephantPath)
	// fmt.Printf("elephant path: %v, cost:%d gain:%d\n", elephantPath, cost, gain)

	return totalGain
}

func Solve() (int, int) {
	ParseInput()

	var distances *[N][N]int = ComputeDistancesMatrix()
	// PrintDistancesMatrix(distances)
	// PrintDistances(distances)

	// part1 := Part1(30, distances)
	part1, _ := Part1_Backtracking(0, distances)

	part2 := Part2_Split(26, 0, distances)

	return part1, part2 // 1651 / 1720, 1707 / 2582
}
