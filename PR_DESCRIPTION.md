# PR 2: Exploration Tab - Graph Visualization Integration

## Summary
Integrates the graph visualization component into the Exploration tab (sales clerk view), placing it alongside the recommendation ticket.

## Changes
- **frontend/components/exploration_tab.py**: Modified to use two-column layout with graph visualization

## Features

### Two-Column Layout
| Column | Content | Width |
|--------|---------|-------|
| Left | Recommendation ticket (product picker + proposals) | 5/9 |
| Right | Interactive graph visualization | 4/9 |

### Real-Time Highlighting
- Fetches reachability data on product selection
- Highlights reachable nodes in teal, unreachable in muted colors
- Selected product marked with ★ in marigold

### Auto-Refresh on Analysis Actions
When user clicks "Explorar con BFS", "Explorar con DFS", or "Ver alcanzabilidad":
1. Fetches new analysis data
2. Calls `load_data()` to refresh session state
3. Triggers `st.rerun()` to update visualization

## Code Changes

### Added Imports
```python
from frontend.components.graph_visualization import render_graph_visualization
from frontend.utils.helpers import api_request, format_pct, load_data
```

### Layout Change
```python
# Before: single column
ticket_col, _free_col = st.columns([5, 4], gap="large")

# After: visualization in right column
ticket_col, graph_col = st.columns([5, 4], gap="large")
with graph_col:
    ui.page_header("Red de conexiones", f"Visualización interactiva desde {product_name}")
    render_graph_visualization(
        graph_data,
        selected_product_id=product_id,
        reachable_products=reachable_ids,
        depth=2
    )
```

### Reachability Fetch
```python
reachability_data, _ = api_request("GET", f"/explore/reachability/{product_id}?depth=2")
reachable_ids = [r['product_id'] for r in reachability_data.get('reachable', [])]
```

## User Experience
1. Sales clerk selects product from ticket dropdown
2. Left panel shows: "Ofrézcale" (direct) + "También le puede interesar" (indirect)
3. Right panel shows: Live network graph with selected product highlighted
4. Clerk can explore BFS/DFS/reachability - graph updates automatically

## Testing
```bash
streamlit run frontend/app.py
# Navigate to "Recomendaciones" → Select product → See graph on right
```