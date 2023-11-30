package main

import (
	_ "embed"
	"fmt"
	"strings"
)

//go:embed input.txt
var input string

const BASE = 5

func SnafuToInt(snafu string) int {
	k := 0
	n := 0
	for i := 0; i < len(snafu); i++ {
		c := snafu[i]

		switch c {
		case '2':
			k = 2
		case '1':
			k = 1
		case '0':
			k = 0
		case '-':
			k = -1
		case '=':
			k = -2
		}

		n = n*BASE + k
	}
	return n
}

func IntToSnafu(value int) string {
	s := ""
	d := value
	r := 0
	for value != 0 {
		r = 0
		d = value % BASE
		if d > 2 {
			d = d - 5
			r = 1
		}

		switch d {
		case -2:
			s = "=" + s
		case -1:
			s = "-" + s

		case 0:
			s = "0" + s

		case 1:
			s = "1" + s

		case 2:
			s = "2" + s
		}

		value = (value + r*BASE) / BASE
	}
	return s
}

func ParseInput() []string {
	return strings.Split(input, "\n")
}

func Part1(snafus []string) int {
	sum := 0
	for i := 0; i < len(snafus); i++ {
		value := SnafuToInt(snafus[i])
		sum += value
	}
	return sum
}

var TEST_SNAFUS []string = []string{"1", "2", "1=", "1-", "10", "11", "12", "2=", "2-", "20", "1=0", "1-0", "1=11-2", "1-0---0", "1121-1110-1=0"}
var TEST_VALUES []int = []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 2022, 12345, 314159265}

func TestConversionSnafuToInt() {
	for i := 0; i < len(TEST_SNAFUS); i++ {
		value := SnafuToInt(TEST_SNAFUS[i])
		if value != TEST_VALUES[i] {
			fmt.Printf("Test failed for %s, expected %d got %d\n", TEST_SNAFUS[i], TEST_VALUES[i], value)
		}
	}
}

func TestConversionIntToSnafu() {

	for i := 0; i < len(TEST_VALUES); i++ {
		snafu := IntToSnafu(TEST_VALUES[i])
		if snafu != TEST_SNAFUS[i] {
			fmt.Printf("Test failed for %d, expected %s got %s\n", TEST_VALUES[i], TEST_SNAFUS[i], snafu)
		}
	}
}

func Solve() string {
	// TestConversionSnafuToInt()
	// TestConversionIntToSnafu()
	snafus := ParseInput()
	part1 := IntToSnafu(Part1(snafus)) // 4890, 32405707664897 (2=222-2---22=1=--1-2)
	return part1
}
