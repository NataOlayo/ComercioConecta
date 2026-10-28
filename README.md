# PR 1: Core Graph Algorithm Enhancements

## Resumen
Mejora significativa de los algoritmos de grafo en `graph.py` para soportar la Feature 2: Exploración de relaciones. Los cambios añaden capacidades de análisis de paths, clasificación semántica de relaciones y análisis de alcanzabilidad.

## Archivos Modificados
- `ComercioConecta/graph.py` (~120 líneas agregadas)

## Cambios Detallados

### 1. Nuevo método `_nivel_relacion(distance)` (líneas ~127-140)
```python
def _nivel_relacion(self, distance):
    """Clasifica el nivel de relación comercial según la distancia en el grafo."""
    if distance == 1:
        return "directo"
    elif distance == 2:
        return "indirecto"
    else:
        return "lejano"
```
**Propósito:** Proporciona una clasificación semántica entendible por usuarios de negocio en lugar de solo distancias numéricas.

### 2. BFS Mejorado (líneas ~142-180)
**Antes:** Retornaba lista de tuplas `(product, distance, cumulative_weight)`
**Ahora:** Retorna lista de dicts con:
- `product`: objeto Product
- `distance`: int
- `cumulative_weight`: float
- `path`: lista de productos en el camino
- `nivel_relacion`: "directo"/"indirecto"/"lejano"
- `alcanzable`: boolean (siempre True en BFS)

**Cambios clave:**
- Queue ahora incluye `path` para rastrear el camino completo
- Resultados incluyen clasificación semántica y path para visualización 2D
- Ordenamiento consistente: distancia ascendente, peso descendente

### 3. DFS Mejorado (líneas ~182-240)
**Antes:** Retornaba lista de tuplas sin path (por consistencia con BFS viejo)
**Ahora:** Retorna lista de dicts **idénticos en estructura a BFS**

**Cambios clave:**
- Ahora incluye `path`, `nivel_relacion`, `alcanzable` igual que BFS
- Consistencia total entre algoritmos para el frontend
- Documentación actualizada explicando cuándo usar cada uno

### 4. Nuevo método `get_component_of_product(product_id)` (líneas ~262-278)
```python
def get_component_of_product(self, product_id):
    """Retorna el componente conexo que contiene el producto dado."""
```
**Propósito:** Determina si dos productos están en el mismo grupo o son desconectados.

### 5. Nuevo método `get_reachability_summary(start_product_id, max_depth)` (líneas ~280-360)
Retorna dict completo con:
- `start_product_id`, `start_product_name`, `max_depth`
- `total_products`, `reachable_count`, `unreachable_count`
- `component_ids`: IDs del componente del producto origen
- `reachable`: lista detallada de productos alcanzables (con path, nivel, etc.)
- `unreachable`: lista de productos NO alcanzables con:
  - `product_id`, `product_name`
  - `in_same_component`: boolean
  - `reason`: "fuera_del_alcance" (mismo componente, más allá de depth) o "otro_componente"

**Propósito:** Base para endpoint `/explore/reachability` y visualización 2D que muestra productos conectados vs desconectados.

## Impacto en el Sistema

| Componente | Impacto |
|------------|---------|
| API (api.py) | Requiere PR 2 para exponer nuevos campos |
| Frontend | Puede mostrar path, nivel_relacion, alcanzables vs no alcanzables |
| Tests | Requiere PR 3 para validar nuevos comportamientos |
| Docs | Requiere PR 4 para documentar nuevos métodos |

## Validación
```bash
# Ejecutar tests existentes (Feature 1)
python -m pytest test_exploration.py -v

# Verificar que BFS/DFS retornan nueva estructura
python -c "
from graph import ProductGraph
from models import Product
g = ProductGraph()
g.add_product(Product('P1', 'Leche'))
g.add_product(Product('P2', 'Pan'))
g.add_relationship('P1', 'P2', 0.8)
result = g.bfs('P1', 2)
print(result[0].keys())  # Debe incluir: product, distance, cumulative_weight, path, nivel_relacion, alcanzable
"
```

## Notas de Implementación
- **Sin dependencias externas**: Algoritmos propios según guía común
- **Backward compatibility**: API cambia formato (requiere PR 2 coordinado)
- **Performance**: BFS/DFS O(V+E) sin cambios en complejidad
- **Memory**: Path tracking añade O(depth) por resultado, aceptable para depth ≤ 4