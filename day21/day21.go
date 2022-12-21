package main

import (
	"bufio"
	_ "embed"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

type Node struct {
	name    string
	op      byte
	number  int
	monkey1 *Node
	monkey2 *Node
}

func (current *Node) eval() int {
	switch current.op {
	case 'v':
		return current.number
	case '+':
		return current.monkey1.eval() + current.monkey2.eval()
	case '-':
		return current.monkey1.eval() - current.monkey2.eval()
	case '*':
		return current.monkey1.eval() * current.monkey2.eval()
	case '/':
		return current.monkey1.eval() / current.monkey2.eval()
	}
	panic("invalid node")
}

var nodes map[string]*Node

func getNode(name string) (node *Node, existing bool) {
	if node, ok := nodes[name]; ok {
		return node, ok
	} else {
		newNode := &Node{name: name}
		nodes[name] = newNode
		return newNode, false
	}
}

func ParseInput() int {
	nodes = make(map[string]*Node)

	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		line := scanner.Text()

		name := line[:4]

		currentNode, _ := getNode(name)
		// if existing {
		// 	panic("already known node named " + name)
		// }

		if len(line) == 3*4+1+4 {
			op := line[11]
			monkey1 := line[6:10]
			monkey2 := line[13:17]

			currentNode.op = op
			node1, _ := getNode(monkey1)
			currentNode.monkey1 = node1
			node2, _ := getNode(monkey2)
			currentNode.monkey2 = node2
			//			fmt.Printf("%s, %s, %c, %s\n", name, monkey1, op, monkey2)
		} else {
			number, _ := strconv.Atoi(line[6:])
			//			fmt.Println(name, number)
			currentNode.op = 'v'
			currentNode.number = number
		}
	}

	return 0
}

func Part1() int {
	return 0
}

func Part2() int {
	return 0
}

func Solve() (int, int) {
	ParseInput()

	part1 := nodes["root"].eval()
	part2 := 0
	return part1, part2
}
