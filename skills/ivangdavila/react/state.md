# State Traps

## Mutation

- `array.push()` + `setState(array)` = no re-render — misma referencia
- `obj.prop = x` + `setState(obj)` = no re-render — misma referencia
- Nested mutation: `obj.deep.value = x` — aunque hagas spread del outer
- `setState(state)` con misma referencia = no re-render, pero no error

## Batching

- Multiple setState en event handler = un solo re-render — batched
- setState en setTimeout/Promise antes de React 18 = múltiples renders
- flushSync fuerza render inmediato — raro necesitarlo pero existe
- State updates en mismo batch usan mismo snapshot de state

## Initialization

- useState en loop = mismos valores cada iteración si no son únicos
- Initial state function con side effects = solo primera vez
- useState(undefined) vs useState() = diferente para TypeScript
- useState(props) como initial — nunca se actualiza cuando props cambia

## Derived State

- State duplicando props = out of sync cuando props cambia
- Computar en render vs guardar en state — preferir computar
- useEffect para sincronizar state con props = un render de delay
- key prop para resetear state cuando entidad cambia

## Lifting State

- State muy arriba = re-renders innecesarios en todo el subtree
- State muy abajo = prop drilling cuando otros componentes lo necesitan
- Context para evitar drilling pero también re-renders — balance necesario

## Forms

- Controlled input sin onChange = readonly pero no parece
- Uncontrolled con defaultValue después de mount = no actualiza
- Checkbox/radio value vs checked — comportamiento diferente
- File input solo puede ser uncontrolled — value es readonly
