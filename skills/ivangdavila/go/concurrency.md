# Concurrency Traps

## Goroutine Lifecycle

- Goroutine without exit condition = runs forever—always have `ctx.Done()` or channel close
- `go func()` captures variables by reference—loop variable trap: `go func(i int)` not `go func()`
- Goroutine started in init() runs before main—may not have expected state
- No way to kill goroutine from outside—must cooperate via context/channel

## Channel Sizing

- Unbuffered = synchronization point—sender waits for receiver
- Buffer size 1 ≠ async—still blocks when full
- "Just make it buffered" hides bugs—understand why it's blocking first
- Buffer size should match expected concurrent senders

## Select Traps

- `select` with multiple ready cases picks randomly—not first listed
- Empty `select{}` blocks forever—useful for blocking main
- `default` makes select non-blocking—careful with busy loops
- Nil channel in select is ignored—useful for disabling cases dynamically

## Mutex Patterns

- `defer mu.Unlock()` right after `mu.Lock()`—don't do work between
- Lock/unlock in same function—avoid passing locked mutex
- `RWMutex` only helps when reads >> writes—otherwise overhead
- Copying struct with mutex copies unlocked mutex—always pass pointer

## Atomic Operations

- `atomic.Value` for copy-on-write patterns—Store must be same type
- Atomic read + atomic write ≠ atomic read-modify-write—use `AddInt64`
- Mixing atomic and non-atomic access = data race—all access must be atomic

## Context Traps

- `context.TODO()` left in production = no cancellation works—replace before shipping
- Context values wrong type = silent nil on retrieve—use typed keys
- Deriving from cancelled context = child already cancelled—check parent first
