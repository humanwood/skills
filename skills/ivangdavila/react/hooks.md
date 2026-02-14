# Hooks Traps

## useState

- `useState(expensiveInit)` ejecuta CADA render — usar `useState(() => expensiveInit)`
- `setState(obj)` no mergea — reemplaza completo, spread manual necesario
- `setState(prev + 1)` con closure stale — usar `setState(prev => prev + 1)`
- State update es async — el valor no cambia hasta siguiente render

## useEffect

- Async function como effect = warning — crear async dentro y llamar
- Return async function como cleanup = no funciona — cleanup debe ser sync
- `[]` deps vacío pero usa variables externas = closure stale
- Object/array en deps = loop infinito (nueva referencia cada render)

## useRef

- `ref.current` cambio no triggerea re-render — a propósito pero confuso
- `useRef(initialValue)` — initial solo primera vez, después ignorado
- Ref en conditional render = ref puede ser null — chequear siempre
- Asignar ref.current en render = mala práctica — usar en effects/handlers

## useCallback

- Sin deps = nueva función cada render — no sirve de nada
- Deps incompletos = callback con valores stale — bugs sutiles
- useCallback en CADA función = premature optimization — solo para memoized children

## useMemo

- Deps incompletos = valor memoizado stale
- Expensive computation que no es expensive = overhead sin beneficio
- Object como dep = siempre recalcula (useMemo en el objeto también)
- useMemo puede ser purgado por React — no para side effects

## useContext

- Context change re-renderiza TODOS los consumers — aunque usen parte diferente
- Default value de createContext solo usado si no hay Provider
- Context en mismo componente que Provider no ve el valor — un nivel abajo

## Custom Hooks

- Nombre sin "use" prefix = ESLint rules no aplican — bugs de deps
- Return array vs object — array para posicional, object para named
- Hook dentro de conditional = violation de rules of hooks
