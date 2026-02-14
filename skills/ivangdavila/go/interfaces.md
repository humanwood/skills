# Interface Traps

## Nil Interface Trap

- `var p *MyType = nil; var i interface{} = p` → `i != nil` is TRUE
- Interface is nil only when BOTH type AND value are nil
- Returning `nil` pointer as interface returns non-nil interface
- Check with `i == nil || reflect.ValueOf(i).IsNil()`—ugly but correct

## Interface Satisfaction

- Pointer receiver on value type doesn't satisfy interface—`*T` has method, `T` doesn't
- Adding method to interface breaks all implementers—interface segregation matters
- Interface satisfaction is implicit—no compile error if method signature drifts slightly
- Empty interface accepts nil—`var i interface{} = nil` then `i == nil` is true

## Type Assertion Traps

- Assertion without ok panics—`s := i.(string)` crashes if not string
- Type switch doesn't work with generic types—use reflect for `T`
- Asserting to interface type checks method set—not underlying type
- `any` type assertion always succeeds—`x.(any)` is pointless

## Embedding Traps

- Embedded interface = "has a", not "is a"—not inheritance
- Embedded nil pointer exposes methods that panic—check before calling
- Shadowing embedded method is silent—no override warning
- Embedding pointer to interface is almost always wrong

## Design Traps

- Interface with 10+ methods = nobody implements it—break into smaller interfaces
- `any` parameter then type switch = runtime panic if unexpected type—loses compile-time safety
- Returning interface hides concrete methods—caller can't access type-specific methods without assertion
