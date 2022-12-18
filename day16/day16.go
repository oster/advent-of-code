package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/edwingeng/deque/v2"
)

//go:embed input.txt
var input string

const N = 59 //10 //59

func min(a int, b int) (int, int) {
	if a < b {
		return a, b
	} else {
		return b, a
	}
}

func Contains(values []string, val string) bool {
	for i := 0; i < len(values); i++ {
		if values[i] == val {
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
		sort.SliceStable(valves, func(i int, j int) bool {
			return valves[i].id < valves[j].id
		})
	}
}

const TIMEOUT_PART1 = 30

func Part1(distances *[N][N]int) int {
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

		// action = all moves
		for idxValve := range valves {
			if idxValve == currentState.location {
				// we do not move
				// action = open the vanne
				if !currentState.valveStates[currentState.location] && valves[currentState.location].flow > 0 {
					newState := currentState
					newState.t += 1
					newState.valveStates[currentState.location] = true
					UpdateProduction(&newState, 1)

					// we "memoize" this new state
					if newState.t <= TIMEOUT_PART1 {
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
			if currentState.t+distances[currentState.location][idxValve] > TIMEOUT_PART1 {
				// skip if out of time
				continue
			}

			newState := currentState
			newState.location = idxValve
			newState.t += distances[currentState.location][idxValve]
			UpdateProduction(&newState, distances[currentState.location][idxValve])

			// we "memoize" this new state
			if newState.t <= TIMEOUT_PART1 {
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
		jump := TIMEOUT_PART1 - newState.t
		newState.t = TIMEOUT_PART1
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

type StateElephant struct {
	t               [2]int
	lastTime        [2]int
	location        [2]int
	candidateValves [2]int
	valveStates     [N]bool
	production      int
}

func PrintReportStateElephant(state *StateElephant) {
	fmt.Println("== Minute", state.t[0], state.t[1], "==")

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
		fmt.Println("releasing", GetInstantPressureElephant(state), "pressure")
	}

}

func GetInstantPressureElephant(state *StateElephant) int {
	pressure := 0
	for i := 0; i < N; i++ {
		if state.valveStates[i] {
			pressure += valves[i].flow
		}
	}
	return pressure
}

func UpdateProductionPart2(state *StateElephant, player int, upToTime int) {
	kTimes := (upToTime - state.lastTime[player])
	//	kTimes1 := (upToTime - state.lastTime[1])
	for i := 0; i < N; i++ {
		if state.valveStates[i] {
			state.production += kTimes * valves[i].flow
			//			state.production += kTimes1 * valves[i].flow
		}
	}
	state.lastTime[0] = upToTime
	state.lastTime[1] = upToTime
}

func PlayAction(distances *[N][N]int, CurrentStates []StateElephant, player int) []StateElephant {
	var NewStates []StateElephant = make([]StateElephant, 0)

	for _, currentState := range CurrentStates {

		// action = all moves
		for idxValve := range valves {
			if idxValve == currentState.location[player] {
				// we do not move
				// action = open the vanne
				if !currentState.valveStates[currentState.location[player]] && valves[currentState.location[player]].flow > 0 {
					newState := currentState
					newState.lastTime[player] = newState.t[player]
					newState.t[player] += 1
					newState.valveStates[currentState.location[player]] = true
					newState.candidateValves[player] = -1
					NewStates = append(NewStates, newState)
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
			if currentState.t[player]+distances[currentState.location[player]][idxValve] > TIMEOUT_PART2 {
				// skip if out of time
				continue
			}

			if player == 0 {
				if currentState.candidateValves[1] == idxValve {
					// skip already target of other player
					continue
				}
			} else {
				if currentState.candidateValves[0] == idxValve {
					// skip already target of other player
					continue
				}
			}

			newState := currentState
			newState.location[player] = idxValve
			newState.lastTime[player] = newState.t[player]
			newState.t[player] += distances[currentState.location[player]][idxValve]
			newState.candidateValves[player] = idxValve

			NewStates = append(NewStates, newState)
		}

		// action = wait till the end
		newState := currentState
		newState.lastTime[player] = newState.t[player]
		newState.t[player] = TIMEOUT_PART2

		NewStates = append(NewStates, newState)
	}
	return NewStates
}

const TIMEOUT_PART2 = 26

func Part2(distances *[N][N]int) int {
	var currentState = StateElephant{t: [2]int{1, 1}, location: [2]int{0, 0}, production: 0, lastTime: [2]int{1, 1}, candidateValves: [2]int{-1, -1}}
	states := deque.NewDeque[StateElephant]()

	states.PushBack(currentState)

	var visitedState map[StateElephant]bool = make(map[StateElephant]bool)

	maxProd := 0

	for !states.IsEmpty() {
		currentState = states.PopFront()

		if currentState.t[0] <= currentState.t[1] {
			UpdateProductionPart2(&currentState, 0, currentState.t[0])
		} else {
			UpdateProductionPart2(&currentState, 1, currentState.t[1])
		}

		// PrintReportStateElephant(&currentState)

		if currentState.production > maxProd {
			maxProd = currentState.production
			// if maxProd > 100 {
			// 	fmt.Println("-->", maxProd)
			// }
		}

		var NewStates []StateElephant = make([]StateElephant, 0)
		NewStates = append(NewStates, currentState)
		NewStates = PlayAction(distances, NewStates, 0)
		// fmt.Println(".->", NewStates)
		NewStates = PlayAction(distances, NewStates, 1)
		// fmt.Println("-->", NewStates)
		for _, newState := range NewStates {
			if newState.t[0] <= TIMEOUT_PART2 && newState.t[1] <= TIMEOUT_PART2 {
				_, ok := visitedState[newState]
				if !ok {
					visitedState[newState] = true
					states.PushBack(newState)
				}
			}
		}
	}

	return maxProd
}

func Permutations(arr []int) [][]int {
	var helper func([]int, int)
	res := [][]int{}

	helper = func(arr []int, n int) {
		if n == 1 {
			tmp := make([]int, len(arr))
			copy(tmp, arr)
			res = append(res, tmp)
		} else {
			for i := 0; i < n; i++ {
				helper(arr, n-1)
				if n%2 == 1 {
					tmp := arr[i]
					arr[i] = arr[n-1]
					arr[n-1] = tmp
				} else {
					tmp := arr[0]
					arr[0] = arr[n-1]
					arr[n-1] = tmp
				}
			}
		}
	}
	helper(arr, len(arr))
	return res
}

func Part1UsingPermutations(distances *[N][N]int) int {
	var useFullValvesIndex []int = GetIndexesOfValvesWithPositivePressure()

	perms := Permutations(useFullValvesIndex)

	startValveIndex := 0 // 0 for sample.txt // 2 for input.txt
	max := 0

	for _, p := range perms {
		gain := 0
		cost := 0

		p = append([]int{startValveIndex}, p...)

		for i := 1; i < len(p); i++ {
			t := distances[p[i-1]][p[i]] + 1
			cost += t
			gain += (30 - cost) * valves[p[i]].flow
		}
		if gain > max {
			max = gain
		}
	}

	return max
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

func Part1_Backtracking(startValveIndex int, distances *[N][N]int) int {
	var valvesIndex []int = GetIndexesOfValvesWithPositivePressure()
	bestGain = 0
	var taken []bool = make([]bool, len(valvesIndex))
	Part1_Backtracking_Solver(valvesIndex, []int{startValveIndex}, distances, 0, 0, 0, taken)
	return bestGain
}

func Part1_Backtracking_Solver(valvesIndex []int, path []int, distances *[N][N]int, depth int, cost int, gain int, taken []bool) {
	if depth > len(valvesIndex) {
		// do we need to evaluate the solution ?
		return
	}

	if depth > 0 {
		// evaluate and store if better
		t := distances[path[depth-1]][path[depth]] + 1
		cost += t
		gain += (30 - cost) * valves[path[depth]].flow

		if cost > 30 {
			return
		}

		if gain > bestGain {
			bestGain = gain
		}
	}

	for i := 0; i < len(valvesIndex); i++ {
		if taken[i] {
			continue
		}
		taken[i] = true
		path = append(path, valvesIndex[i])
		Part1_Backtracking_Solver(valvesIndex, path, distances, depth+1, cost, gain, taken)
		taken[i] = false
		path = path[:len(path)-1]
	}
}

func Solve() (int, int) {
	ParseInput()

	var distances *[N][N]int = ComputeDistancesMatrix()

	// PrintDistancesMatrix(distances)
	// PrintDistances(distances)

	// part1 := 0
	// part1 := Part1(distances)
	// part1 := Part1UsingPermutations(distances)
	part1 := Part1_Backtracking(0, distances)

	part2 := 0
	// part2 := Part2(distances)

	return part1, part2 // 1651 / 1720 (6 sec.), ?
}
