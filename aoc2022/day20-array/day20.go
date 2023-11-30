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

const size = 5000

func ParseInput() (numbers [size]int) {

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	idx := 0
	for scanner.Scan() {
		n, _ := strconv.Atoi(scanner.Text())
		numbers[idx] = n
		idx++
	}

	return numbers
}

func GetValues(numbers [size]int, indexes [size]int) (values [size]int) {
	for j := 0; j < len(numbers); j++ {
		values[indexes[j]] = numbers[j]
	}
	return values
}

func PrintValues(numbers [size]int, indexes [size]int) {
	var values [size]int = GetValues(numbers, indexes)

	fmt.Print("[ ")
	for j := 0; j < len(numbers); j++ {
		fmt.Print(values[j], " ")
	}
	fmt.Println("]")
}

func Part1(numbers [size]int) int {
	var indexes [size]int

	for i := 0; i < size; i++ {
		indexes[i] = i
	}

	for index := 0; index < size; index++ {
		shift := numbers[index]
		newIndex := (indexes[index] + shift + 2*(size-1)) % (size - 1)

		if newIndex == 0 {
			newIndex = size - 1
		}

		if shift == 0 {
			continue
		}

		oldIndex := indexes[index]
		indexes[index] = newIndex

		for otherIndex := 0; otherIndex < size; otherIndex++ {
			if otherIndex == index {
				continue
			}

			indexOfOtherIndex := indexes[otherIndex]
			if oldIndex > newIndex && indexOfOtherIndex >= newIndex && indexOfOtherIndex < oldIndex {
				indexes[otherIndex]++
			} else {
				if indexOfOtherIndex >= oldIndex && indexOfOtherIndex <= newIndex {
					indexes[otherIndex]--
				}
			}
		}
	}

	values := GetValues(numbers, indexes)
	indexOfZero := -1
	for i := 0; i < size; i++ {
		if values[i] == 0 {
			indexOfZero = i
			break
		}
	}

	a := values[(indexOfZero+1000)%size] // should be 4
	b := values[(indexOfZero+2000)%size] // should be -3
	c := values[(indexOfZero+3000)%size] // should be 2

	return a + b + c // should be 3 for sample
}

func Part2(numbers [size]int) int {
	encryptionKey := 811589153

	var indexes [size]int

	for i := 0; i < size; i++ {
		numbers[i] *= encryptionKey
		indexes[i] = i
	}

	for k := 0; k < 10; k++ {
		// for index, shift := range numbers {
		for index := 0; index < size; index++ {
			shift := numbers[index]
			newIndex := (indexes[index] + shift + 10*encryptionKey*(size-1)) % (size - 1)

			if newIndex == 0 {
				newIndex = size - 1
			}

			if shift == 0 {
				continue
			}

			oldIndex := indexes[index]
			indexes[index] = newIndex

			for otherIndex := 0; otherIndex < size; otherIndex++ {
				if otherIndex == index {
					continue
				}

				indexOfOtherIndex := indexes[otherIndex]
				if oldIndex > newIndex && indexOfOtherIndex >= newIndex && indexOfOtherIndex < oldIndex {
					indexes[otherIndex]++
				} else {
					if indexOfOtherIndex >= oldIndex && indexOfOtherIndex <= newIndex {
						indexes[otherIndex] = (indexOfOtherIndex - 3 + 2*size) % (size - 1)
					}
				}
			}
		}
	}

	values := GetValues(numbers, indexes)
	indexOfZero := -1
	for i := 0; i < size; i++ {
		if values[i] == 0 {
			indexOfZero = i
			break
		}
	}

	a := values[(indexOfZero+1000)%size] // should be 4
	b := values[(indexOfZero+2000)%size] // should be -3
	c := values[(indexOfZero+3000)%size] // should be 2

	return a + b + c // should be 3 for sample
}

func Solve() (int, int) {
	numbers := ParseInput()

	part1 := Part1(numbers) // 3, 27726
	part2 := Part2(numbers)
	return part1, part2
}
