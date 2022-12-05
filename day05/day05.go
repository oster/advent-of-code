package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"time"
)

//go:embed input.txt
var input string

func PrintTopOfStacks(stacks []ByteStack) {
	for _, s := range stacks {
		fmt.Print(string(s[len(s)-1]))
	}
	fmt.Println()
}

func PrintStacks(stacks []ByteStack) {
	fmt.Print("[")
	for _, stack := range stacks {
		fmt.Print(string(" [" + stack.ToString() + "]"))
	}
	fmt.Println(" ]")
}

type Move struct {
	count int
	src   int
	dst   int
}

func ParseInput() ([]ByteStack, []Move) {
	var stacks []ByteStack = make([]ByteStack, 0)
	var moves []Move = make([]Move, 0)

	var move_parsing bool = false

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
					stacks = append(stacks, NewStack())
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

	return stacks, moves
}

func Solve() ([]ByteStack, []ByteStack) {
	var stacks []ByteStack
	var stacks2 []ByteStack
	var moves []Move

	stacks, moves = ParseInput()

	stacks2 = make([]ByteStack, len(stacks))
	for i, stack := range stacks {
		stacks2[i] = stack.Copy()
	}

	// Part 1
	for _, move := range moves {
		for i := 0; i < move.count; i++ {
			c := stacks[move.src-1].Pop()
			stacks[move.dst-1].Push(c)
		}
	}

	// Part 2
	var tmpStack = NewStack()
	for _, move := range moves {
		for i := 0; i < move.count; i++ {
			tmpStack.Push(stacks2[move.src-1].Pop())
		}

		for i := 0; i < move.count; i++ {
			stacks2[move.dst-1].Push(tmpStack.Pop())
		}
	}

	return stacks, stacks2
}

func main() {
	start := time.Now()
	stacks, stacks2 := Solve()
	fmt.Println(time.Since(start))

	PrintTopOfStacks(stacks)
	PrintTopOfStacks(stacks2)
}
