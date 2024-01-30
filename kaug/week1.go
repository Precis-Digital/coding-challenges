package kaug

import (
	_ "embed" // for embedding input files
	"fmt"
	"strconv"
	"strings"
)

func init() {
	RegisterWeek(&Week1{}, WeekName1)
}

var _ IWeek = (*Week1)(nil)

// WeekName1 is a name of week 1.
const WeekName1 WeekName = "1"

// Week1 is
type Week1 struct {
	Week
}

// Run returns the answer of the week.
func (w *Week1) Run() (string, error) {
	answers := make([]string, 4)

	answers[0] = solveWeek1E(1)
	answers[1] = solveWeek1E(2)
	answers[2] = solveWeek1H(1)
	answers[3] = solveWeek1H(2)

	return fmt.Sprintf("%v", answers), nil
}

//go:embed inputs/week1E.txt
var inputWeek1E string

func solveWeek1E(part int) string {
	rows := strings.Split(inputWeek1E, "\n")
	sum := 0
	for _, row := range rows {
		if row == "" {
			continue
		}
		sum += calcFuel(row, part)
	}
	return fmt.Sprintf("%d", sum)
}

func calcFuel(s string, part int) int {
	num, _ := strconv.Atoi(s)
	fuel := num/3 - 2
	if part == 1 {
		return fuel
	}
	if fuel <= 0 {
		return 0
	}
	return fuel + calcFuel(fmt.Sprintf("%d", fuel), part)
}

//go:embed inputs/week1H.txt
var inputWeek1H string

func solveWeek1H(part int) string {
	return "TODO"
}
