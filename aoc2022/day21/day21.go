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

type Node struct {
	name    string
	op      byte
	number  int
	monkey1 *Node
	monkey2 *Node
}

func (current *Node) Eval() int {
	switch current.op {
	case 'v':
		return current.number
	case 'm':
		return current.number
	case '+':
		return current.monkey1.Eval() + current.monkey2.Eval()
	case '-':
		return current.monkey1.Eval() - current.monkey2.Eval()
	case '*':
		return current.monkey1.Eval() * current.monkey2.Eval()
	case '/':
		a := current.monkey1.Eval()
		b := current.monkey2.Eval()
		if a%b != 0 {
			panic("gloups")
		}
		return a / b
	case '=':
		return current.monkey1.Eval() - current.monkey2.Eval()
	}
	panic("invalid node")
}

func (current *Node) Reduce() *Node {
	if current.name == "humn" { // we do not reduce this not according to Part 2
		return current
	}

	if current.op == 'v' {
		return current
	}

	current.monkey1 = current.monkey1.Reduce()
	current.monkey2 = current.monkey2.Reduce()

	if current.op == '=' {
		return current
	}

	if current.monkey1.op == 'v' && current.monkey2.op == 'v' {
		switch current.op {
		case '+':
			current.number = current.monkey1.number + current.monkey2.number
		case '-':
			current.number = current.monkey1.number - current.monkey2.number
		case '*':
			current.number = current.monkey1.number * current.monkey2.number
		case '/':
			current.number = current.monkey1.number / current.monkey2.number
			if current.number*current.monkey2.number != current.monkey1.number {
				panic("gloups: " + fmt.Sprintf("%v", current.monkey1.number) + " is not divisible by " + fmt.Sprintf("%v", current.monkey2.number))
			}

		case '=':
		}
		current.op = 'v'
	}

	return current
	// panic("invalid node")
}

func (current *Node) Solve(value int) int {

	if current.op == 'm' {
		return value
	}

	if current.monkey1.op == 'v' && current.monkey2.op != 'v' {
		switch current.op {
		case '+':
			return current.monkey2.Solve(value - current.monkey1.number)
		case '-':
			return current.monkey2.Solve(-(value - current.monkey1.number))
		case '*':
			if value%current.monkey1.number != 0 {
				panic("gloups: " + fmt.Sprintf("%v", value) + " is not divisible by " + fmt.Sprintf("%v", current.monkey1.number))
			}
			return current.monkey2.Solve(value / current.monkey1.number)
		case '/':
			return current.monkey2.Solve(value * current.monkey1.number)
		case '=', 'm':
			panic("this type of node should not be present in the expression to solve")
		}
	}

	if current.monkey1.op != 'v' && current.monkey2.op == 'v' {
		switch current.op {
		case '+':
			return current.monkey1.Solve(value - current.monkey2.number)
		case '-':
			return current.monkey1.Solve(value + current.monkey2.number)
		case '*':
			if value%current.monkey2.number != 0 {
				panic("gloups: " + fmt.Sprintf("%v", value) + " is not divisible by " + fmt.Sprintf("%v", current.monkey2.number))
			}
			return current.monkey1.Solve(value / current.monkey2.number)
		case '/':
			return current.monkey1.Solve(value * current.monkey2.number)
		case 'm':
			return value // we found the variable, so we know the result ;)
		case '=':
			panic("this type of node should not be present in the expression to solve")
		}
	}

	panic("should not happen")
}

func (current *Node) ToString() string {
	if current.op == 'v' {
		return fmt.Sprintf("%v", current.number)
	}

	if current.op == 'm' {
		return "?"
	}
	return fmt.Sprintf("(%s %c %s)", current.monkey1.ToString(), current.op, current.monkey2.ToString())
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

	// fmt.Println(nodes["root"].ToString())
	part1 := nodes["root"].Eval() // 152, 276156919469632

	part2 := 0
	nodes["root"].op = '='
	nodes["humn"].op = 'm'

	root := nodes["root"]
	root.Reduce() // left node will contains the simplified expression, right node the expected result
	// fmt.Println(nodes["root"].ToString())

	part2 = root.monkey1.Solve(root.monkey2.Eval()) // 301, 3441198826073

	return part1, part2
}
