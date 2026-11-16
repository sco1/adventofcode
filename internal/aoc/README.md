# internal/aoc

Shared helpers for Go puzzle solutions, imported as:

```go
import "github.com/sco1/adventofcode/internal/aoc"
```

Each Go solution lives in its day's `go/` folder (e.g. `2015/Day_01/go/`) as a `package main`, and any code used by more than one day belongs here instead of being copied between days.

## Why `internal`

Go only allows a package under an `internal` folder to be imported by code inside the folder that contains it. Because this one sits at the repo root, every day in the module can import it, but other modules can't.
