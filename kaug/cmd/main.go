package main

import (
	"fmt"
	"kaug"
)

func main() {
	weeks := kaug.Weeks
	for name, week := range weeks {
		week.StartTimer()
		answer, err := week.Run()
		if err != nil {
			fmt.Printf("week=%s err=%v\n", name, err)
			continue
		}
		week.EndTimer()
		ms := float64(week.GetDuration().Nanoseconds()) / 1e6
		fmt.Printf("week=%s answer=%s duration=%0.3fms\n", name, answer, ms)
	}
}
