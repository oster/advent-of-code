package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

func min(a int, b int) (int, int) {
	if a < b {
		return a, b
	} else {
		return b, a
	}
}

func abs(a int) int {
	if a >= 0 {
		return a
	}
	return -a
}

type Window struct {
	x1 int
	y1 int
	x2 int
	y2 int
}

func NewWindow() *Window {
	return &Window{math.MaxInt, math.MaxInt, math.MinInt, math.MinInt}
}

func (current *Window) Update(newX int, newY int) {
	current.x1, _ = min(current.x1, newX)
	_, current.x2 = min(newX, current.x2)
	current.y1, _ = min(current.y1, newY)
	_, current.y2 = min(newY, current.y2)

}

var window *Window = NewWindow()

func ManhattanDistance(x1 int, y1 int, x2 int, y2 int) int {
	return abs(x1-x2) + abs(y1-y2)
}

type Beacon struct {
	x int
	y int
}

func NewSensor(sensorX int, sensorY int, nearestBeacon *Beacon) *Sensor {
	return &Sensor{x: sensorX, y: sensorY, nearestBeacon: nearestBeacon, coveredDistance: ManhattanDistance(sensorX, sensorY, nearestBeacon.x, nearestBeacon.y)}
}

func DumpSensors() {
	for _, sensor := range sensors {
		fmt.Println(*sensor)
	}
}

var beacons []*Beacon = make([]*Beacon, 0)

func BeaconAt(x int, y int) *Beacon {
	for _, beacon := range beacons {
		if beacon.x == x && beacon.y == y {
			return beacon
		}
	}
	return nil
}

func CreateBeaconIfNotExist(x int, y int) *Beacon {
	beacon := BeaconAt(x, y)
	if beacon != nil {
		return beacon
	}

	newBeacon := Beacon{x: x, y: y}
	beacons = append(beacons, &newBeacon)
	return &newBeacon

}

type Sensor struct {
	x               int
	y               int
	nearestBeacon   *Beacon
	coveredDistance int
}

var sensors []*Sensor = make([]*Sensor, 0)

func SensorAt(x int, y int) *Sensor {
	for _, sensor := range sensors {
		if sensor.x == x && sensor.y == y {
			return sensor
		}
	}
	return nil
}

func SortSensors() {
	sort.Slice(sensors, func(i int, j int) bool {
		return sensors[i].coveredDistance > sensors[j].coveredDistance
	})
}

func ParseInput() {
	scanner := bufio.NewScanner(strings.NewReader(input))
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		fields := strings.Split(scanner.Text(), " ")

		beaconX, _ := strconv.Atoi(fields[8][2 : len(fields[8])-1])
		beaconY, _ := strconv.Atoi(fields[9][2:])
		beacon := CreateBeaconIfNotExist(beaconX, beaconY)

		window.Update(beaconX, beaconY)

		sensorX, _ := strconv.Atoi(fields[2][2 : len(fields[2])-1])
		sensorY, _ := strconv.Atoi(fields[3][2 : len(fields[3])-1])

		window.Update(sensorX, sensorY)

		sensors = append(sensors, NewSensor(sensorX, sensorY, beacon))
	}
}

var mapping [][]byte

func DumpMap() {

	for y := window.y1; y < window.y2; y++ {
		for x := window.x1; x < window.x2; x++ {
			switch mapping[y-window.y1][x-window.x1] {
			case 'S':
				fmt.Print("S")
			case 'B':
				fmt.Print("B")
			default:
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func GenerateMap() {
	// generate Map reporting Sensors/Beacons
	mapping = make([][]byte, window.y2-window.y1+1)
	for y := window.y1; y < window.y2; y++ {
		mapping[y-window.y1] = make([]byte, window.x2-window.x1+1)
	}

	for y := window.y1; y < window.y2; y++ {
		for x := window.x1; x < window.x2; x++ {
			if SensorAt(x, y) != nil {
				mapping[y-window.y1][x-window.x1] = 'S'
				continue
			}
			if BeaconAt(x, y) != nil {
				mapping[y-window.y1][x-window.x1] = 'B'
				continue
			}
		}
	}
}

func BruteForcePart1(scanY int) int {
	maxCoveredRange := 0
	for _, sensor := range sensors {
		if sensor.coveredDistance > maxCoveredRange {
			maxCoveredRange = sensor.coveredDistance
		}
	}

	// var scanLine []byte = make([]byte, (window.x2+maxCoveredRange)-(window.x1-maxCoveredRange))
	xUpperBound := window.x2 + maxCoveredRange
	// shiftX := maxCoveredRange - window.x1

	count := 0

	for x := window.x1 - maxCoveredRange; x < xUpperBound; x++ {
		if SensorAt(x, scanY) != nil {
			// scanLine[x+shiftX] = 'S'
			continue
		}
		if BeaconAt(x, scanY) != nil {
			// scanLine[x+shiftX] = 'B'
			continue
		}

		for _, sensor := range sensors {
			if sensor.coveredDistance >= ManhattanDistance(sensor.x, sensor.y, x, scanY) {
				// scanLine[x+shiftX] = '#'
				count++
				break
			}
		}
	}

	return count
}

func ScanLine(scanY int, upperBound int, beaconChannel chan *Beacon) {
	var scanX int = -1
	for scanX <= upperBound {
		scanX++

		if SensorAt(scanX, scanY) != nil {
			continue
		}
		if BeaconAt(scanX, scanY) != nil {
			continue
		}

		covered := false
		for _, sensor := range sensors {
			d := sensor.coveredDistance - ManhattanDistance(sensor.x, sensor.y, scanX, scanY)

			if d >= 0 {
				covered = true
				scanX += d
				break
			}
		}
		if !covered {
			//fmt.Println(scanX*4000000 + scanY)
			beaconChannel <- &Beacon{scanX, scanY}
		}
	}
}

func BruteForcePart2(upperBound int) int {
	var beaconChannel chan *Beacon = make(chan *Beacon)
	defer close(beaconChannel)

	var distressBeacon *Beacon = nil
	var tuningFrequency int = -1
	for scanY := 0; scanY <= upperBound; scanY++ {
		go ScanLine(scanY, upperBound, beaconChannel)
	}

	distressBeacon = <-beaconChannel
	tuningFrequency = distressBeacon.x*4000000 + distressBeacon.y
	return tuningFrequency
}

func Solve() (int, int) {
	ParseInput()
	SortSensors()
	// DumpSensors()

	// GenerateMap()
	// DumpMap()

	// part1 := BruteForcePart1(10) // 26 for sample.txt
	// part2 := BruteForcePart2(20) // (14,11) 56000011 for sample
	part1 := BruteForcePart1(2000000) // 5181556 to low
	part2 := BruteForcePart2(4000000) // (14,11) 56000011 for sample
	return part1, part2               // 26 / 5181556, (14,11) 56000011 / (3204400,3219131) 12817603219131
}
