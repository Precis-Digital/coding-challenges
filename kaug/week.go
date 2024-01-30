package kaug

import (
	"fmt"
	"time"
)

// WeekName is a type that represents a week name.
type WeekName string

// ErrNotImplemented is an error that represents a function is not implemented.
var ErrNotImplemented = fmt.Errorf("not implemented")

// IWeek is an interface that represents a week.
type IWeek interface {
	Run() (string, error)
	StartTimer() time.Time
	EndTimer() time.Time
	GetDuration() time.Duration
}

// Week is a struct that represents a week.
type Week struct {
	Week      int
	StartedAt time.Time
	EndedAt   time.Time
	Duration  time.Duration
}

// StartTimer returns the started time of the week.
func (w *Week) StartTimer() time.Time {
	now := time.Now()
	w.StartedAt = now
	return w.StartedAt
}

// EndTimer returns the ended time of the week.
func (w *Week) EndTimer() time.Time {
	now := time.Now()
	w.EndedAt = now
	w.Duration = time.Since(w.StartedAt)
	return w.EndedAt
}

// GetDuration returns the duration of the week.
func (w *Week) GetDuration() time.Duration {
	return w.Duration
}

// Weeks is a list of all weeks.
var Weeks = make(map[WeekName]IWeek)

// RegisterWeek registers a week.
func RegisterWeek(w IWeek, name WeekName) {
	Weeks[name] = w
}

// fmtAnswers formats answers.
func fmtAnswers(answers []string) string {
	return fmt.Sprintf("%v", answers)
}
