# PR 3: Feature 2 Acceptance Tests

## Resumen
Nuevo archivo de pruebas de aceptación comprehensivo para Feature 2: `acceptance_test_feature2.py`. Valida todos los escenarios requeridos por la especificación de Feature 2.

## Archivos Nuevos
- `ComercioConecta/acceptance_test_feature2.py` (~457 líneas - archivo completo nuevo)

## Escenarios de Prueba Cubiertos

### 1. ESCENARIO NORMAL: BFS y DFS desde producto con conexiones
- BFS desde producto con relaciones (Leche/P001) profundidad 2
- Verifica: productos alcanzables esperados presentes (Pan, Huevos, Mantequilla, Café)
- Verifica: **todos los resultados tienen `nivel_relacion`**
- Verifica: **todos los resultados tienen `path`**
- DFS desde mismo producto
- Verifica: **DFS devuelve `path` completo**

### 2. ESCENARIO: Grafo Vacío (sin productos)
- BFS desde producto inexistente en grafo vacío → 404
- Reachability desde producto inexistente en grafo vacío → 404
- Componentes en grafo vacío → 0 componentes

### 3. ESCENARIO: Producto Inexistente
- BFS desde P999 → 404
- DFS desde P999 → 404
- Reachability desde P999 → 404

### 4. ESCENARIO: Producto Aislado (sin relaciones)
- BFS desde P009 (Sal, aislado) → 0 resultados
- Verifica: **no inventa recomendaciones** para productos sin conexiones

### 5. ESCENARIO: Ruta/Relación Inexistente (Profundidad Insuficiente)
- BFS desde P009 (aislado) no alcanza otros productos
- BFS desde P001 profundidad 1 → **NO alcanza P004 (Mantequilla, distancia 2)**

### 6. ESCENARIO: Datos Inválidos (Profundidad)
- BFS con depth=0 → 400
- BFS con depth=-1 → 400
- DFS con depth=0 → 400
- Reachability con depth=-1 → 400

### 7. ESCENARIO: Componentes Conexos (Grupos Desconectados)
- Listar componentes → **≥ 2 componentes esperados**
- Verifica: **Producto aislado P009 en su propio componente**

### 8. ESCENARIO: Reachability - Alcanzables vs No Alcanzables
- Reachability desde P001 (Leche) profundidad 2
- Verifica: **alcanzables correctos** (P002, P003, P004, P005)
- Verifica: **no alcanzables correctos** (P007, P008, P009 - otros componentes)
- Verifica: **todos los no alcanzables tienen campo `reason`**
  - `"fuera_del_alcance"`: mismo componente pero más allá de max_depth
  - `"otro_componente"`: componente diferente
- Verifica: **conteos consistentes** (reachable_count == len(reachable), etc.)

## Datos de Prueba (Seed)

El test crea un grafo representativo:
```
Productos (9): P001-P009
  P001: Leche        P005: Café
  P002: Pan          P006: Azúcar
  P003: Huevos       P007: Aceite
  P004: Mantequilla  P008: Arroz
  P009: Sal (aislado)

Relaciones (9):
  Leche-Pan (0.85)      Café-Azúcar (0.80)
  Leche-Huevos (0.70)   Aceite-Arroz (0.75)
  Pan-Mantequilla (0.90) Leche-Café (0.40)
  Huevos-Mantequilla (0.65) Pan-Huevos (0.55)

Componentes:
  Componente 1: {P001, P002, P003, P004, P005, P006} - 6 productos conectados
  Componente 2: {P007, P008} - 2 productos conectados
  Componente 3: {P009} - 1 producto aislado
```

## Ejecución

```bash
# Asegurar que API esté corriendo en puerto 5000
python api.py &

# Ejecutar tests Feature 2
python acceptance_test_feature2.py

# Resultado esperado:
# ====================================================================
# RESUMEN: XX/XX pruebas pasaron
# [OK] Todas las pruebas de aceptación de Feature 2 pasaron!
```

## Códigos de Salida
- `0`: Todas las pruebas pasaron
- `1`: Una o más pruebas fallaron

## Métricas de Cobertura

| Categoría | Tests | Qué Valida |
|-----------|-------|------------|
| Funcionalidad Core | 4 | BFS/DFS estructura, path, nivel_relacion |
| Edge Cases | 5 | Grafo vacío, producto inexistente, aislado, profundidad insuficiente |
| Validación | 4 | Depth 0, negativo en BFS/DFS/Reachability |
| Componentes | 2 | Múltiples componentes, producto aislado en componente propio |
| Reachability | 4 | Alcanzables, no alcanzables, reasons, conteos |

**Total: ~19 aserciones verificadas**

## Dependencias

**Requiere:** PR 1 + PR 2 (graph.py y api.py con funcionalidad Feature 2 completa)

## Integración con CI/CD

```yaml
# Ejemplo GitHub Actions
- name: Run Feature 2 Acceptance Tests
  run: |
    python api.py &
    sleep 3
    python acceptance_test_feature2.py
  # Exit code 1 fallará el job si hay fallos
```

## Notas

- **Archivo nuevo cohesivo**: No se divide naturalmente en PRs menores
- **Ligeramente > 400 líneas** (~457): Se mantiene junto por cohesión funcional
- **Auto-limpieza**: `delete_all_products()` al inicio de cada escenario mayor
- **Logging detallado**: Cada test imprime expected vs obtained para debugging
- **Compatible**: No modifica `acceptance_test.py` (Feature 1 intacto)