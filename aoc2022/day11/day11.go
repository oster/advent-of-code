package main

import (
	_ "embed"
	"fmt"
	"sort"

	"github.com/edwingeng/deque/v2"
)

type Monkey struct {
	id                int
	items             *deque.Deque[int]
	operate           func(int) int
	divisibleByValue  int
	monkeyDstTrue     *Monkey
	monkeyDstFalse    *Monkey
	inspectionCounter int
}

func NewMonkey(id int, op func(int) int, divisor int, items []int) Monkey {
	res := Monkey{
		id:                id,
		operate:           op,
		divisibleByValue:  divisor,
		inspectionCounter: 0}

	res.items = deque.NewDeque[int]()

	for _, item := range items {
		res.items.PushBack(item)
	}

	return res
}

func (current *Monkey) ToString() string {
	return fmt.Sprintf("Monkey(%d, /%d, counter:%d, [%v])", current.id, current.divisibleByValue, current.inspectionCounter, current.items.Dump())
}

func (current *Monkey) Bind(monkeyTrue *Monkey, monkeyFalse *Monkey) {
	current.monkeyDstTrue = monkeyTrue
	current.monkeyDstFalse = monkeyFalse
}

func (current *Monkey) Inspect(ppm int) {
	// fmt.Println("Before: ", current.ToString())
	for !current.items.IsEmpty() {
		current.inspectionCounter++

		item := current.items.PopFront()
		item = current.operate(item)

		if ppm == 0 {
			item = item / 3 // div by 3 then round to the nearest int
		} else {
			// failure!
			// if item >= 96577 { // 23 * 19 * 13 * 17 = 96577
			// 	item = item - 96577 // (11 * 7 * 3 * 5 * 17 * 13 * 19 * 2) = 9699690
			// }
			item = item % ppm
		}

		if item%current.divisibleByValue == 0 {
			current.monkeyDstTrue.items.PushBack(item)
		} else {
			current.monkeyDstFalse.items.PushBack(item)
		}
	}
	// fmt.Println("After: ", current.ToString())
}

func SampleData() []Monkey {
	var monkeys []Monkey = make([]Monkey, 4)

	monkeys[0] = NewMonkey(0,
		func(old int) int { return old * 19 },
		23,
		[]int{79, 98},
	)
	monkeys[1] = NewMonkey(1,
		func(old int) int { return old + 6 },
		19,
		[]int{54, 65, 75, 74},
	)
	monkeys[2] = NewMonkey(2,
		func(old int) int { return old * old },
		13,
		[]int{79, 60, 97},
	)
	monkeys[3] = NewMonkey(3,
		func(old int) int { return old + 3 },
		17,
		[]int{74},
	)

	monkeys[0].Bind(&monkeys[2], &monkeys[3])
	monkeys[1].Bind(&monkeys[2], &monkeys[0])
	monkeys[2].Bind(&monkeys[1], &monkeys[3])
	monkeys[3].Bind(&monkeys[0], &monkeys[1])

	return monkeys
}

func PuzzleData() []Monkey {
	var monkeys []Monkey = make([]Monkey, 8)

	monkeys[0] = NewMonkey(0,
		func(old int) int { return old * 3 },
		11,
		[]int{50, 70, 54, 83, 52, 78},
	)
	monkeys[1] = NewMonkey(1,
		func(old int) int { return old * old },
		7,
		[]int{71, 52, 58, 60, 71},
	)
	monkeys[2] = NewMonkey(2,
		func(old int) int { return old + 1 },
		3,
		[]int{66, 56, 56, 94, 60, 86, 73},
	)
	monkeys[3] = NewMonkey(3,
		func(old int) int { return old + 8 },
		5,
		[]int{83, 99},
	)
	monkeys[4] = NewMonkey(4,
		func(old int) int { return old + 3 },
		17,
		[]int{98, 98, 79},
	)
	monkeys[5] = NewMonkey(5,
		func(old int) int { return old + 4 },
		13,
		[]int{76},
	)
	monkeys[6] = NewMonkey(6,
		func(old int) int { return old * 17 },
		19,
		[]int{52, 51, 84, 54},
	)
	monkeys[7] = NewMonkey(7,
		func(old int) int { return old + 7 },
		2,
		[]int{82, 86, 91, 79, 94, 92, 59, 94},
	)

	monkeys[0].Bind(&monkeys[2], &monkeys[7])
	monkeys[1].Bind(&monkeys[0], &monkeys[2])
	monkeys[2].Bind(&monkeys[7], &monkeys[5])
	monkeys[3].Bind(&monkeys[6], &monkeys[4])
	monkeys[4].Bind(&monkeys[1], &monkeys[0])
	monkeys[5].Bind(&monkeys[6], &monkeys[3])
	monkeys[6].Bind(&monkeys[4], &monkeys[1])
	monkeys[7].Bind(&monkeys[5], &monkeys[3])

	return monkeys
}

func Iterate(monkeys []Monkey, endRound int, ppm int) int {
	for round := 1; round <= endRound; round++ {
		for i := 0; i < len(monkeys); i++ {
			monkeys[i].Inspect(ppm)
		}

		// if round == 1 || round == 20 || round%1000 == 0 {
		// 	fmt.Println("== After round ", round, " ==")
		// 	for _, monkey := range monkeys {
		// 		fmt.Println(monkey.ToString())
		// 	}
		// }
	}

	// var inspectionCounters []int = make([]int, len(monkeys))
	// for i, monkey := range monkeys {
	// 	inspectionCounters[i] = monkey.inspectionCounter
	// }
	// sort.Sort(sort.Reverse(sort.IntSlice(inspectionCounters)))
	// return inspectionCounters[0] * inspectionCounters[1]

	sort.SliceStable(monkeys, func(i, j int) bool {
		return monkeys[i].inspectionCounter > monkeys[j].inspectionCounter
	})
	return monkeys[0].inspectionCounter * monkeys[1].inspectionCounter
}

func Solve() (int, int) {
	// var dataFactory func() []Monkey = SampleData
	var dataFactory func() []Monkey = PuzzleData

	// stop at round 20, relief using / 3
	part1 := Iterate(dataFactory(), 20, 0)

	monkeys := dataFactory()
	ppm := 1
	for _, monkey := range monkeys {
		ppm *= monkey.divisibleByValue
	}
	// stop at round 10000, relief using % ppm (Π divisor_i)
	part2 := Iterate(monkeys, 10000, ppm)

	return part1, part2 // 10605/102399 , 2713310158 = 52166 * 52013 / 23641658401
}
