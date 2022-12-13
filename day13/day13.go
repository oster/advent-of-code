package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"sort"
	"strings"

	"github.com/edwingeng/deque/v2"
)

//go:embed input.txt
var input string

type Packet struct {
	payload []*Packet
	value   int
}

func NewPacket() *Packet {
	res := Packet{}
	res.payload = make([]*Packet, 0)
	res.value = -1
	return &res
}

func NewPacketFromInt(value int) *Packet {
	res := Packet{}
	res.payload = nil
	res.value = value
	return &res
}

func (current *Packet) ToString() string {
	if current.payload != nil {
		return SliceOfPacketToString(current.payload)
	} else {
		return fmt.Sprintf("%v", current.value)
	}
}

func SliceOfPacketToString(packets []*Packet) string {
	res := "["
	for idx, packet := range packets {
		res += packet.ToString()
		if idx < len(packets)-1 {
			res += ","
		}
	}
	res += "]"
	return res
}

type PacketPair struct {
	left  *Packet
	right *Packet
}

func (current Packet) LesserThan(another Packet) int {
	if current.value != -1 && another.value != -1 {
		// both are integer
		if current.value < another.value {
			return -1
		} else if current.value > another.value {
			return +1
		} else {
			// we need to compare the rest of the outer packet
			return 0
		}
	} else if current.value == -1 && another.value != -1 {

		return -another.LesserThan(current) // reverse the comparison

	} else if current.value != -1 && another.value == -1 {
		tmp := NewPacket()
		tmp.payload = append(tmp.payload, NewPacketFromInt(current.value))
		return tmp.LesserThan(another)

	}

	// current.value == -1 && current.value == -1
	// both are list
	idx := 0
	for idx < len(current.payload) && idx < len(another.payload) {
		// fmt.Print(".")
		cmp := current.payload[idx].LesserThan(*another.payload[idx])
		if cmp != 0 {
			return cmp
		}
		idx++
	}
	if idx >= len(current.payload) {
		return -1
	}
	if idx >= len(another.payload) {
		return 1
	}

	panic("unreachable statement")
}

func ParsePacket(line string) *Packet {
	var value int = -1 // we assume there is no value -1 in the packet payloard
	stack := deque.NewDeque[*Packet]()

	var current *Packet = nil

	for _, c := range line {
		switch c {
		case '[':
			if current != nil {
				stack.PushBack(current)
			}
			current = NewPacket()
		case ']':
			if value != -1 {
				current.payload = append(current.payload, NewPacketFromInt(value))
				value = -1
			}
			if !stack.IsEmpty() {
				tmp := current
				current = stack.PopBack()
				current.payload = append(current.payload, tmp)
			} else {
				return current
			}
		case ',':
			if value != -1 {
				current.payload = append(current.payload, NewPacketFromInt(value))
				value = -1
			}
		default:
			// expect [0-9]
			if value == -1 {
				value = 0
			}
			value = value*10 + int(c-'0')
		}
	}

	panic("invalid packet description")
}

func ParseInput() []PacketPair {
	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	res := make([]PacketPair, 0)

	for scanner.Scan() {
		packet1 := ParsePacket(scanner.Text())
		scanner.Scan()
		packet2 := ParsePacket(scanner.Text())
		res = append(res, PacketPair{packet1, packet2})
		scanner.Scan() // skip line
	}

	return res
}

func Solve() (int, int) {
	packetPairs := ParseInput()

	// Part 1

	part1 := 0
	for idx, pair := range packetPairs {
		cond := pair.left.LesserThan(*pair.right)
		if cond == -1 {
			part1 += (idx + 1)
		}
	}

	// Part 2

	allPackets := make([]*Packet, 0)
	for _, pair := range packetPairs {
		allPackets = append(allPackets, pair.left)
		allPackets = append(allPackets, pair.right)
	}

	dividerPacket1 := ParsePacket("[[2]]")
	dividerPacket2 := ParsePacket("[[6]]")
	allPackets = append(allPackets, dividerPacket1)
	allPackets = append(allPackets, dividerPacket2)

	sort.Slice(allPackets, func(i int, j int) bool {
		return allPackets[i].LesserThan(*allPackets[j]) == -1
	})

	var idx1 int
	var idx2 int
	for idx, packet := range allPackets {
		if packet == dividerPacket1 {
			idx1 = idx
		} else if packet == dividerPacket2 {
			idx2 = idx
		}
	}

	part2 := (idx1 + 1) * (idx2 + 1)

	return part1, part2 // 13 / 5825, 140 / 24477
}
