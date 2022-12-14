package main

import (
	_ "embed"
	"strconv"
	"strings"
	"text/scanner"
)

func Min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func Max(x, y int) int {
	if x > y {
		return x
	}
	return y
}

//go:embed input.txt
var input string

func SolveEmbed() (int, int) {
	fullyOverlapCount := 0
	partialOverlapCount := 0

	type IdRange struct {
		start int
		end   int
	}

	var elf1 IdRange
	var elf2 IdRange

	var s scanner.Scanner
	s.Init(strings.NewReader(input))
	s.Whitespace |= 1<<'-' | 1<<','

	for tok := s.Scan(); tok != scanner.EOF; tok = s.Scan() {
		elf1.start, _ = strconv.Atoi(s.TokenText())
		s.Scan()
		elf1.end, _ = strconv.Atoi(s.TokenText())
		s.Scan()
		elf2.start, _ = strconv.Atoi(s.TokenText())
		s.Scan()
		elf2.end, _ = strconv.Atoi(s.TokenText())

		if (elf1.start <= elf2.start && elf1.end >= elf2.end) || (elf2.start <= elf1.start && elf2.end >= elf1.end) {
			fullyOverlapCount++
		}

		if !(elf1.end < elf2.start || elf2.end < elf1.start) {
			// if (elf1.end >= elf2.start && elf1.start <= elf2.end) || (elf2.end >= elf1.start && elf2.start <= elf1.end) {
			// if Max(elf1.start, elf2.start) <= Min(elf1.end, elf2.end) {
			partialOverlapCount++
		}
	}

	return fullyOverlapCount, partialOverlapCount
}
