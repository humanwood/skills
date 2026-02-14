# Error Handling Traps

## Wrapping Traps

- `fmt.Errorf("context: %w", err)` wraps—`%v` loses the chain
- `errors.Is(err, target)` checks chain—`==` only checks exact match
- `errors.As(err, &target)` extracts from chain—pointer to pointer required
- Re-wrapping already wrapped error creates deeper chain—may be intentional

## Sentinel Error Traps

- `errors.New()` creates new instance each call—define once as `var`
- `var ErrNotFound = errors.New("not found")` at package level
- Comparing to sentinel with `==` fails if wrapped—use `errors.Is`
- Sentinel errors are part of API—changing text is breaking change

## Error Checking Traps

- `if err != nil { return err }` loses context—wrap with `%w`
- Ignoring error with `_` is silent bug—linter should catch
- Checking `err == nil` then using result—may still be zero value
- Multiple returns: `val, err := f()` — `val` may be valid even when `err != nil`

## Panic/Recover Traps

- Panic in goroutine crashes entire program—recover only helps in same goroutine
- `recover()` only works in deferred function—not in regular call
- Panic for bugs, error for expected failures—don't panic on user input
- `recover()` returns `nil` if no panic—check before using

## Custom Error Traps

- Error type should be pointer receiver—`*MyError` not `MyError`
- `Unwrap()` method enables `errors.Is/As`—forget and chain breaks
- Returning `(*MyError)(nil)` returns non-nil error interface—same trap as interface nil

## Logging Traps

- `log.Fatal` calls `os.Exit(1)`—defers don't run
- `log.Panic` panics after logging—may be caught by recover
- Logging error then returning it = duplicate logs
- Format string with `%+v` for stack traces (if using pkg/errors)
