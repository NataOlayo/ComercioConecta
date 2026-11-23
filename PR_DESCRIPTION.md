# PR 1: Graph Visualization Component

## Summary
Adds interactive graph visualization for the commercial network using NetworkX and PyVis.

## Changes
- **requirements.txt**: Added `networkx>=3.2` and `pyvis>=0.3` dependencies
- **frontend/components/graph_visualization.py**: New component with two visualization functions

## Features

### `render_graph_visualization(graph_data, selected_product_id, reachable_products, depth)`
Interactive force-directed graph showing:
- **Nodes**: Products (circles sized by connection count)
- **Edges**: Co-purchase relationships (width proportional to weight)
- **Color coding**:
  - 🟡 Marigold (★): Selected product
  - 🟢 Teal: Reachable within depth limit
  - ⚪ Muted: Unreachable (other component or beyond depth)
- **Interactions**: Pan, zoom, hover tooltips, navigation buttons
- **Physics**: ForceAtlas2-based layout for organic clustering

### `render_component_visualization(components_data)`
Displays connected components as expandable groups with product chips.

## Technical Details
- NetworkX used **only for visualization** (per project guidelines)
- Actual graph algorithms (BFS, DFS, components) remain in `graph.py`
- PyVis generates standalone HTML embedded via `st.components.v1.html`
- Fallback text visualization if PyVis fails

## API Endpoints Consumed
- `GET /graph/info` - Full graph structure (products + relationships)
- `GET /explore/reachability/<id>?depth=<n>` - Reachable/unreachable classification

## Testing
Run with API at `http://127.0.0.1:5000`:
```bash
streamlit run frontend/app.py
```
Navigate to "Recomendaciones" tab to see visualization in right column.