package main

import (
	"bufio"
	_ "embed"
	"errors"
	"log"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

const DIRECTORY_TYPE byte = 1
const FILE_TYPE byte = 2

type FSNode struct {
	fstype   byte
	size     uint
	name     string
	parent   *FSNode
	children []*FSNode
}

func NewFS(filename string) *FSNode {
	node := FSNode{
		fstype:   DIRECTORY_TYPE,
		name:     filename,
		size:     0,
		parent:   nil,
		children: nil}
	return &node
}

func (node *FSNode) AddDir(directoryName string) *FSNode {
	dir := NewFS(directoryName)
	if node.children == nil {
		node.children = make([]*FSNode, 0)
	}
	dir.parent = node
	dir.fstype = DIRECTORY_TYPE
	node.children = append(node.children, dir)

	return dir
}

func (node *FSNode) AddFile(fileName string, fileSize uint) *FSNode {
	file := NewFS(fileName)
	if node.children == nil {
		node.children = make([]*FSNode, 0)
	}
	file.parent = node
	file.fstype = FILE_TYPE
	file.size = fileSize
	node.children = append(node.children, file)
	// node.children[fileName] = file

	return file
}

func (node *FSNode) ChangeDir(directoryName string) (*FSNode, error) {
	for _, child := range node.children {
		if child.name == directoryName {
			return child, nil
		}
	}
	return nil, errors.New("Directory not found when cd " + directoryName)
}

func (node *FSNode) DiskUse() uint {
	if node.fstype == FILE_TYPE || node.children == nil {
		return node.size
	}
	for _, child := range node.children {
		node.size += child.DiskUse()
	}
	return node.size
}

func (node *FSNode) Part1() uint {
	var sum uint

	if node.fstype == FILE_TYPE || node.children == nil {
		return 0
	}
	for _, child := range node.children {
		sum += child.Part1()
	}
	if node.size < 100000 {
		sum += node.size
	}
	return sum
}

func (node *FSNode) Part2(sizeToClear uint, min *FSNode) *FSNode {
	if node.fstype == FILE_TYPE || node.size < sizeToClear || node.children == nil {
		return min
	}
	for _, child := range node.children {
		min = child.Part2(sizeToClear, min)
	}
	if node.size < min.size {
		min = node
	}
	return min
}

func BuildTree(description string) *FSNode {
	root := NewFS("/")
	pwd := root

	scanner := bufio.NewScanner(strings.NewReader(description))
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		line := scanner.Text()
		if line[0] == '$' {
			switch line[2] {
			case 'c': // cd command
				path := line[5:]
				switch path {
				case "/":
					pwd = root
				case "..":
					pwd = pwd.parent
				default:
					var err error
					pwd, err = pwd.ChangeDir(path)
					if err != nil {
						log.Fatalln(err)
					}
				}
			case 'l': // ls command

			default:
				log.Fatalln("Unkown command")
			}
		} else {
			if line[0] == 'd' { // directory
				fileName := line[4:]
				pwd.AddDir(fileName)
			} else { // file
				i := 0
				for line[i] <= '9' {
					i++
				}
				fileSize, err := strconv.Atoi(line[:i-1])
				if err != nil {
					log.Fatalln("invalid size", line[:i-1])
				}
				fileName := line[i:]
				pwd.AddFile(fileName, uint(fileSize))
			}
		}
	}

	return root
}

func Solve() (uint, uint) {
	root := BuildTree(input)
	root.DiskUse()

	part1 := root.Part1() // 1391690

	diskSpace := uint(70000000)
	neededSpace := uint(30000000) // at least
	diskUse := root.size
	unusedSpace := diskSpace - diskUse
	neededSpaceToClear := neededSpace - unusedSpace

	part2 := root.Part2(neededSpaceToClear, root).size // 5469168

	return part1, part2
}
