# Pattern Traps

## Conditional Rendering

- `{count && <Component />}` renderiza "0" cuando count es 0 — usar `count > 0 &&`
- `{condition ? <A /> : <B />}` — mismo componente type = state preservado
- `{items.length && <List />}` — 0 rendered, usar `items.length > 0`
- undefined en JSX = nada, pero null explícito más claro

## Keys

- Key prop en componente padre no afecta children — key es para siblings
- Key cambiada = unmount + mount — útil para reset pero destruye state
- Key debe ser del data, no derivada del índice
- Fragmentos con key necesitan `<React.Fragment key>`, no `<>` shorthand

## Props

- Spreading props `{...props}` puede pasar props no deseados a DOM
- Boolean attribute: `disabled` = `disabled={true}`, no `disabled="false"`
- className, no class — error común de HTML a JSX
- htmlFor, no for — para labels

## Refs

- Ref en function component sin forwardRef = warning
- useImperativeHandle sin forwardRef = no funciona
- Ref callback se llama con null en unmount — handle null case
- Refs no disponibles en primer render — useEffect para acceder

## Error Boundaries

- Solo class components pueden ser error boundaries — no hooks
- Error en event handler no es capturado — solo render/lifecycle
- Error boundary no captura errores async — try/catch necesario
- Error en boundary mismo = error propaga hacia arriba

## Portals

- Portal children fuera de DOM hierarchy pero EN React hierarchy
- Events bubble en React tree, no DOM tree — confuso para stopPropagation
- Portal sin target element en SSR = error — conditional render necesario
- Context disponible en portal aunque DOM esté afuera
