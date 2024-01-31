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

// solveWeek1E solves week 1, easy part.
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

type position struct {
	x, y, z int
}

type moon struct {
	position position
	velocity position
	gravity  position
}

type frequency struct {
	x, y, z int
}

type state struct {
	x, y, z string
}

// solveWeek1H solves week 1, hard part.
func solveWeek1H(part int) string {
	moons := make([]moon, 0)
	for _, row := range strings.Split(inputWeek1H, "\n") {
		if row == "" {
			continue
		}
		moons = append(moons, parseMoon(row))
	}

	if part == 1 {
		for i := 0; i < 1000; i++ {
			applyGravity(moons, nil)
		}
		return fmt.Sprintf("%d", calcEnergy(moons))
	}

	var x, y, z string
	for _, m := range moons {
		x += fmt.Sprint(m.position.x)
		y += fmt.Sprint(m.position.y)
		z += fmt.Sprint(m.position.z)
	}

	var f frequency
	for step := 2; ; step++ {
		var s state
		applyGravity(moons, &s)
		if s.x == x && f.x == 0 {
			f.x = step
		}
		if s.y == y && f.y == 0 {
			f.y = step
		}
		if s.z == z && f.z == 0 {
			f.z = step
		}
		if f.x != 0 && f.y != 0 && f.z != 0 {
			break
		}
	}

	return fmt.Sprintf("%d", lcm(lcm(f.x, f.y), f.z))

}

// lcm returns the least common multiple of a and b.
func lcm(a, b int) int {
	return a * b / gcd(a, b)
}

// gcd returns the greatest common divisor of a and b.
func gcd(a, b int) int {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func parseMoon(s string) moon {
	m := moon{}
	fmt.Sscanf(s, "<x=%d, y=%d, z=%d>", &m.position.x, &m.position.y, &m.position.z)
	return m
}

func applyGravity(moons []moon, state *state) {
	for i := 0; i < len(moons); i++ {
		for j := i; j < len(moons); j++ {
			applyGravityBetween(&moons[i], &moons[j])
		}
		applyVelocity(&moons[i], state)
	}
}

func applyGravityBetween(m1, m2 *moon) {
	if m1.position.x < m2.position.x {
		m1.gravity.x++
		m2.gravity.x--
	} else if m1.position.x > m2.position.x {
		m1.gravity.x--
		m2.gravity.x++
	}
	if m1.position.y < m2.position.y {
		m1.gravity.y++
		m2.gravity.y--
	} else if m1.position.y > m2.position.y {
		m1.gravity.y--
		m2.gravity.y++
	}
	if m1.position.z < m2.position.z {
		m1.gravity.z++
		m2.gravity.z--
	} else if m1.position.z > m2.position.z {
		m1.gravity.z--
		m2.gravity.z++
	}
}

func applyVelocity(m *moon, state *state) {
	m.velocity.x += m.gravity.x
	m.velocity.y += m.gravity.y
	m.velocity.z += m.gravity.z
	m.gravity.x, m.gravity.y, m.gravity.z = 0, 0, 0
	m.position.x += m.velocity.x
	m.position.y += m.velocity.y
	m.position.z += m.velocity.z

	if state != nil {
		state.x += fmt.Sprint(m.position.x)
		state.y += fmt.Sprint(m.position.y)
		state.z += fmt.Sprint(m.position.z)
	}
}

func calcEnergy(moons []moon) int {
	sum := 0
	for _, m := range moons {
		pot := abs(m.position.x) + abs(m.position.y) + abs(m.position.z)
		kin := abs(m.velocity.x) + abs(m.velocity.y) + abs(m.velocity.z)
		sum += pot * kin
	}
	return sum
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}
