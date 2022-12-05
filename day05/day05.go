package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"time"
)

//go:embed input.txt
var input string

func PrintTopOfStacks(stacks [][]byte) {
	for _, s := range stacks {
		fmt.Print(string(s[len(s)-1]))
	}
	fmt.Println()
}

func PrintStack(stack []byte) {
	for _, c := range stack {
		fmt.Print(string(c))
	}
	fmt.Println()
}

func PrintStacks(stacks [][]byte) {
	for _, s := range stacks {
		PrintStack(s)
	}
}

func Reverse[T any](original []T) (reversed []T) {
	reversed = make([]T, len(original))
	copy(reversed, original)

	for i := len(reversed)/2 - 1; i >= 0; i-- {
		tmp := len(reversed) - 1 - i
		reversed[i], reversed[tmp] = reversed[tmp], reversed[i]
	}

	return
}

var stacks [][]byte
var stacks2 [][]byte

func Solve() {
	stacks = make([][]byte, 0)

	var move_parsing bool = false

	type Move struct {
		count int
		src   int
		dst   int
	}

	var moves []Move = make([]Move, 0)

	i := 0
	l := len(input)
	stacks_index := 0

	for i < l {
		if !move_parsing {
			// parsing stacks description
			if input[i] == ' ' && input[i+1] != ' ' {
				// skipping...(id of stacks) - juminping to next 2 lines
				for input[i] != 10 {
					i++
				}
				i += 2
				move_parsing = true
			}

			for {
				if stacks_index >= len(stacks) {
					stacks = append(stacks, make([]byte, 0))
				}

				if input[i] == ' ' && input[i+1] == ' ' {
					i += 3
				} else if input[i] == '[' {
					v := input[i+1]
					stacks[stacks_index] = append(stacks[stacks_index], v)
					i += 3
				} else {
					break
				}

				stacks_index++
				i++
				if input[i-1] == 10 {
					stacks_index = 0
					break
				}
			}
		} else {
			// parsing move instructions
			var move Move

			i += 5 // skipping "move "

			j := 0
			for input[i+j] != 32 {
				j++
			}
			move.count, _ = strconv.Atoi(input[i : i+j])
			i += j + 1

			i += 5 // skipping "from "
			j = 0
			for input[i+j] != 32 {
				j++
			}
			move.src, _ = strconv.Atoi(input[i : i+j])

			i += j + 1
			i += 3 // skipping "to "
			j = 0
			for (i+j < l) && input[i+j] != 10 {
				j++
			}
			move.dst, _ = strconv.Atoi(input[i : i+j])

			i += j + 1
			moves = append(moves, move)
		}
	}

	for idx, stack := range stacks {
		stacks[idx] = Reverse(stack)
	}

	stacks2 = make([][]byte, len(stacks))
	for i, stack := range stacks {
		stacks2[i] = make([]byte, len(stack))
		copy(stacks2[i], stack)
	}

	// Part 1
	for _, move := range moves {
		for i := 0; i < move.count; i++ {
			c := stacks[move.src-1][len(stacks[move.src-1])-1]
			stacks[move.src-1] = stacks[move.src-1][:len(stacks[move.src-1])-1]
			stacks[move.dst-1] = append(stacks[move.dst-1], c)
		}
	}

	// Part 2
	var tmpStack = make([]byte, 0)
	for _, move := range moves {
		for i := 0; i < move.count; i++ {
			tmpStack = append(tmpStack, stacks2[move.src-1][len(stacks2[move.src-1])-1])
			stacks2[move.src-1] = stacks2[move.src-1][:len(stacks2[move.src-1])-1]
		}

		for i := 0; i < move.count; i++ {
			stacks2[move.dst-1] = append(stacks2[move.dst-1], tmpStack[len(tmpStack)-1])
			tmpStack = tmpStack[:len(tmpStack)-1]
		}
	}

}

func main() {
	start := time.Now()
	Solve()
	fmt.Println(time.Since(start))
	PrintTopOfStacks(stacks)
	PrintTopOfStacks(stacks2)
}
