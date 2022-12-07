package main

import (
	"bufio"
	_ "embed"
	"log"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

const DIRECTORY_TYPE byte = 1
const FILE_TYPE byte = 2

// type FSNode interface {
// 	Name() string
// 	Size() uint
// 	Parent() *FSDirectory
// 	Part1() uint
// }

type FSFile struct {
	fstype byte
	parent *FSDirectory
	name   string
	size   uint
}

func (node FSFile) Size() uint {
	return node.size
}

func (node FSFile) Name() string {
	return node.name
}

func (node FSFile) Parent() *FSDirectory {
	return node.parent
}

type FSDirectory struct {
	base              FSFile
	childrenDirectory []*FSDirectory
	childrenFile      []*FSFile
}

func (node FSDirectory) Size() uint {
	if node.base.size == 0 {
		for _, child := range node.childrenDirectory {
			node.base.size += (*child).Size()
		}
		for _, child := range node.childrenFile {
			node.base.size += (*child).Size()
		}
	}
	return node.base.size
}

func (node FSDirectory) Name() string {
	return node.base.name
}

func (node FSDirectory) Parent() *FSDirectory {
	return node.base.parent
}

func NewFile(parent *FSDirectory, filename string, fileSize uint) *FSFile {
	node := FSFile{
		fstype: FILE_TYPE,
		parent: parent,
		name:   filename,
		size:   fileSize,
	}
	return &node
}

func NewDirectory(parent *FSDirectory, filename string) *FSDirectory {
	node := FSDirectory{
		base: FSFile{
			fstype: DIRECTORY_TYPE,
			parent: parent,
			name:   filename,
			size:   0},
		childrenDirectory: nil,
		childrenFile:      nil}

	return &node
}

func (node *FSDirectory) AddDir(directoryName string) *FSDirectory {
	dir := NewDirectory(node, directoryName)
	if node.childrenDirectory == nil {
		node.childrenDirectory = make([]*FSDirectory, 0)
	}
	node.childrenDirectory = append(node.childrenDirectory, dir)

	return dir
}

func (node *FSDirectory) AddFile(fileName string, fileSize uint) *FSFile {
	file := NewFile(node, fileName, fileSize)
	if node.childrenFile == nil {
		node.childrenFile = make([]*FSFile, 0)
	}
	node.childrenFile = append(node.childrenFile, file)

	return file
}

func (node *FSDirectory) ChangeDir(directoryName string) *FSDirectory {
	for _, child := range node.childrenDirectory {
		if child.Name() == directoryName {
			return child
		}
	}
	panic("Directory not found when cd " + directoryName + " from " + node.Name())
}

func (node FSDirectory) Part1() uint {
	var sum uint

	for _, child := range node.childrenDirectory {
		sum += child.Part1()
	}
	if node.Size() < 100000 {
		sum += node.Size()
	}
	return sum
}

func (node *FSDirectory) Part2(sizeToClear uint, min *FSDirectory) *FSDirectory {
	if node.Size() < sizeToClear {
		return min
	}

	for _, child := range node.childrenDirectory {
		min = child.Part2(sizeToClear, min)
	}
	if node.Size() < min.Size() {
		min = node
	}
	return min
}

func BuildTree(description string) *FSDirectory {
	var pwd, root *FSDirectory
	root = NewDirectory(nil, "/")
	pwd = root

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
					pwd = pwd.Parent()
				default:
					pwd = pwd.ChangeDir(path)
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
	root.Size()

	part1 := root.Part1() // 1391690

	diskSpace := uint(70000000)
	neededSpace := uint(30000000) // at least
	diskUse := root.Size()
	unusedSpace := diskSpace - diskUse
	neededSpaceToClear := neededSpace - unusedSpace

	part2 := root.Part2(neededSpaceToClear, root).Size() // 5469168

	return part1, part2
}
