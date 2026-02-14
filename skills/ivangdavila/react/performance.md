# Performance Traps

## Re-renders

- Parent re-render = children re-render — aunque props no cambien (sin memo)
- Inline object prop `style={{}}` = nueva referencia cada render
- Inline function prop `onClick={() => {}}` = nueva referencia cada render
- Context value objeto = todos los consumers re-renderizan en cada cambio

## React.memo

- memo con object props sin comparador = siempre re-renderiza
- memo no previene re-render si children cambian
- memo deep comparison custom puede ser más caro que re-render
- Props que son children no se memorizan automáticamente

## useMemo/useCallback

- useMemo tiene overhead — no usar para operaciones triviales
- useCallback sin memoized children que lo consumen = desperdicio
- Dependencies array incompleto = valores stale — peor que no memoizar
- useMemo para objetos en deps de otro useMemo = dependency chain

## Lists

- key={index} con reorder/filter = bugs de estado, animaciones rotas
- key generado en render `key={Math.random()}` = unmount/mount cada render
- key debe ser estable Y único — timestamp puede repetirse
- Missing key = React usa index internamente — mismo problema que key={index}

## Code Splitting

- lazy() de componente muy pequeño = overhead mayor que beneficio
- Suspense fallback muy diferente = layout shift
- Error boundary alrededor de lazy = error handling necesario
- Preload de lazy components = mejor que esperar interacción

## Profiling Gotchas

- Dev mode es MUCHO más lento — profiler en production build
- StrictMode dobla effects — parece más lento de lo que es
- Profiler commit phase no incluye browser paint — métricas incompletas
- React DevTools profiler tiene overhead — no refleja perf real
