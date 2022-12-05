package main

import (
	_ "embed"
	"testing"
)

func Benchmark(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Solve()
	}
}
