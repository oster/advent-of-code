package main

import (
	"testing"
)

func Benchmark(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = Solve()
	}
}

func BenchmarkSet(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = SolveWithSet()
	}
}

func BenchmarkEmbed(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = SolveEmbed()
	}
}
