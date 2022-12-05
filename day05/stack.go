package main

import "fmt"

type ByteStack []byte

func (stack ByteStack) Print() {
	for _, c := range stack {
		fmt.Print(string(c))
	}
	fmt.Println()
}

func NewStack() ByteStack {
	return make([]byte, 0)
}

func (stack ByteStack) Copy() ByteStack {
	stackCopy := make([]byte, len(stack))
	copy(stackCopy, stack)
	return stackCopy
}

func (stack *ByteStack) Pop() byte {
	top := (*stack)[len(*stack)-1]
	*stack = (*stack)[:len(*stack)-1]
	return top
}

func (stack *ByteStack) Push(value byte) {
	*stack = append((*stack), value)
}

func Reverse[T any](original []T) (reversed []T) {
	reversed = make([]T, len(original))
	copy(reversed, original)

	for i := len(reversed)/2 - 1; i >= 0; i-- {
		tmp := len(reversed) - 1 - i
		reversed[i], reversed[tmp] = reversed[tmp], reversed[i]
	}

	return
}
