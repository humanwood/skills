# Slice, Map, String Traps

## Slice Memory Traps

- Slicing doesn't copy—`b := a[1:3]` shares backing array with `a`
- Append may or may not reallocate—never assume capacity unchanged
- Large slice keeps entire backing array alive—copy if extracting small piece
- `append([]int{}, a...)` is the copy idiom—not `copy()` which needs pre-allocation
- Nil slice and empty slice differ—`var s []int` vs `s := []int{}`

## Slice Mutation Traps

- Passing slice to function shares memory—mutations visible to caller
- `append` in function may or may not affect caller—depends on capacity
- Slice of pointers: modifying pointed values affects original
- `clear(s)` zeros elements but keeps length—use `s = s[:0]` to empty

## Map Traps

- Reading nil map returns zero value—writing panics
- Map iteration order is random—don't rely on it for anything
- Maps not safe for concurrent access—use `sync.Map` or mutex
- `&m[key]` doesn't compile—can't take address of map element
- Delete during iteration is safe—but add may skip or revisit

## Map Gotchas

- Struct key must be comparable—no slices/maps inside
- `m[key]++` works—no need to read-modify-write
- Zero value useful—`m[key]` returns `0` for missing int key
- NaN key in map is weird—can insert but never retrieve

## String Traps

- `len(s)` is bytes, not characters—use `utf8.RuneCountInString`
- `s[i]` is byte, not rune—use `for _, r := range s` for runes
- String concatenation in loop is O(n²)—use `strings.Builder`
- Substring shares memory—large string stays alive
- Strings are immutable—every modification allocates

## Conversion Traps

- `[]byte(s)` copies the string—not free for large strings
- `string(65)` is `"A"`—converts int to rune, not to decimal string
- `strconv.Itoa` for int to string—not `string(i)`
