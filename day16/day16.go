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

const N = 59

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

func PrintDistancesMatrix(value *[N][N]int) {
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			fmt.Print(value[i][j], " ")
		}
		fmt.Println()
	}
}

func PrintDistances(distances *[N][N]int) {
	for idxSrc, valveSrc := range valves {
		fmt.Println("From Valve", valveSrc.id)
		for idxDst, valveDst := range valves {
			fmt.Println("   to Valve", valveDst.id, "=", distances[idxSrc][idxDst])
		}
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

func ComputeDistances() *[N][N]int {
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

func Solve() (int, int) {
	ParseInput()

	var adj *[N][N]int = ComputeDistances()
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

	// PrintDistancesMatrix(distances)
	// PrintDistances(distances)

	part1 := Part1(distances)
	// part1 := 0
	// part2 := Part2(distances)
	part2 := 0
	return part1, part2 // 1651 / 1720 (6 sec.), ?
}
