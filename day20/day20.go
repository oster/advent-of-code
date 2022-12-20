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

func ParseInput() (numbers []int) {
	numbers = make([]int, 0)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		n, _ := strconv.Atoi(scanner.Text())
		numbers = append(numbers, n)
	}

	return numbers
}

func GetValues(numbers []int, indexes []int) (values []int) {
	values = make([]int, len(numbers))
	for j := 0; j < len(numbers); j++ {
		values[indexes[j]] = numbers[j]
	}
	return values
}

func PrintValues(numbers []int, indexes []int) {
	var values []int = GetValues(numbers, indexes)

	fmt.Print("[ ")
	for j := 0; j < len(numbers); j++ {
		fmt.Print(values[j], " ")
	}
	fmt.Println("]")
}

func Part1(numbers []int) int {
	size := len(numbers)
	var indexes []int = make([]int, size)

	for i := 0; i < size; i++ {
		indexes[i] = i
	}

	for index, shift := range numbers {
		newIndex := (indexes[index] + shift + 2*(size-1)) % (size - 1)

		if newIndex == 0 {
			newIndex = size - 1
		}

		if shift == 0 {
			continue
		}

		oldIndex := indexes[index]
		indexes[index] = newIndex

		if oldIndex > newIndex {
			for otherIndex := 0; otherIndex < size; otherIndex++ {
				if otherIndex == index {
					continue
				}
				if indexes[otherIndex] >= newIndex && indexes[otherIndex] < oldIndex {
					indexes[otherIndex] = (indexes[otherIndex] + 1)
				}
			}
		} else {
			for otherIndex := 0; otherIndex < size; otherIndex++ {
				if otherIndex == index {
					continue
				}
				if indexes[otherIndex] >= oldIndex && indexes[otherIndex] <= newIndex {
					indexes[otherIndex] = (indexes[otherIndex] - 1)
				}
			}
		}

		// PrintValues(numbers, indexes)
	}

	// fmt.Println(indexes)

	//PrintValues(numbers, indexes)
	values := GetValues(numbers, indexes)
	indexOfZero := -1
	for i := 0; i < size; i++ {
		if values[i] == 0 {
			indexOfZero = i
			break
		}
	}

	a := values[(indexOfZero+1000)%size] // should be 4
	// fmt.Println(a)
	b := values[(indexOfZero+2000)%size] // should be -3
	// fmt.Println(b)
	c := values[(indexOfZero+3000)%size] // should be 2
	// fmt.Println(c)

	return a + b + c // should be 3 for sample
}

func Part2(numbers []int) int {
	encryptionKey := 811589153

	size := len(numbers)
	for i := 0; i < size; i++ {
		numbers[i] *= encryptionKey
	}
	var indexes []int = make([]int, size)

	for i := 0; i < size; i++ {
		indexes[i] = i
	}

	for k := 0; k < 10; k++ {

		for index, shift := range numbers {
			newIndex := (indexes[index] + shift + 10*encryptionKey*(size-1)) % (size - 1)

			if newIndex == 0 {
				newIndex = size - 1
			}

			if shift == 0 {
				continue
			}

			oldIndex := indexes[index]
			indexes[index] = newIndex

			if oldIndex > newIndex {
				for otherIndex := 0; otherIndex < size; otherIndex++ {
					if otherIndex == index {
						continue
					}
					if indexes[otherIndex] >= newIndex && indexes[otherIndex] < oldIndex {
						indexes[otherIndex] = (indexes[otherIndex] + 1)
					}
				}
			} else {
				for otherIndex := 0; otherIndex < size; otherIndex++ {
					if otherIndex == index {
						continue
					}
					if indexes[otherIndex] >= oldIndex && indexes[otherIndex] <= newIndex {
						indexes[otherIndex] = (indexes[otherIndex] - 1 + 2*(size-1)) % (size - 1)
					}
				}
			}

			// PrintValues(numbers, indexes)
		}
	}

	// fmt.Println(indexes)

	//PrintValues(numbers, indexes)
	values := GetValues(numbers, indexes)
	indexOfZero := -1
	for i := 0; i < size; i++ {
		if values[i] == 0 {
			indexOfZero = i
			break
		}
	}

	a := values[(indexOfZero+1000)%size] // should be 4
	fmt.Println(a)
	b := values[(indexOfZero+2000)%size] // should be -3
	fmt.Println(b)
	c := values[(indexOfZero+3000)%size] // should be 2
	fmt.Println(c)

	return a + b + c // should be 3 for sample
}

func Solve() (int, int) {
	numbers := ParseInput()

	part1 := Part1(numbers) // 3, 27726
	part2 := Part2(numbers)
	return part1, part2
}
