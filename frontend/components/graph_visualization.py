"""
Graph Visualization Component for ComercioConecta
==================================================

This module provides interactive graph visualization using NetworkX and PyVis.
It visualizes the commercial graph with products as nodes and co-purchase relationships as edges.
The selected product and its reachable/unreachable products are highlighted.

NetworkX is used only for visualization purposes, as per project guidelines.
The actual graph algorithms (BFS, DFS, components) are implemented in graph.py.
"""

import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from html import escape

from frontend.utils.helpers import format_pct


def render_graph_visualization(graph_data, selected_product_id=None, reachable_products=None, depth=2):
    """
    Render an interactive graph visualization of the commercial network.

    Args:
        graph_data: Dictionary with 'products' and 'relationships' from /graph/info endpoint
        selected_product_id: ID of the currently selected product (to highlight)
        reachable_products: List of reachable product IDs from the selected product
        depth: Maximum depth for reachability (used for labeling)
    """
    if not graph_data or not graph_data.get('products'):
        st.info("No hay productos en la red para visualizar. Registre productos y relaciones primero.")
        return

    # Create NetworkX graph
    G = nx.Graph()

    # Add nodes (products)
    product_names = {}
    for product in graph_data['products']:
        pid = product['id']
        name = product['name']
        product_names[pid] = name
        G.add_node(pid, label=name, title=f"{name} ({pid})")

    # Add edges (relationships)
    for rel in graph_data['relationships']:
        pid_a = rel['product_a']
        pid_b = rel['product_b']
        weight = rel['weight']
        G.add_edge(pid_a, pid_b, weight=weight, title=f"Co-compra: {format_pct(weight)}")

    # Determine node colors and sizes based on selection and reachability
    reachable_set = set(reachable_products) if reachable_products else set()

    # Build PyVis network
    net = Network(
        height="600px",
        width="100%",
        bgcolor="#F3F6F4",
        font_color="#15302E",
        directed=False,
        notebook=False,
        cdn_resources="in_line"
    )

    # Configure physics for better layout
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
          "enabled": true,
          "iterations": 150,
          "updateInterval": 25
        }
      },
      "nodes": {
        "font": {
          "size": 14,
          "face": "IBM Plex Sans",
          "color": "#15302E"
        },
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "shape": "dot",
        "scaling": {
          "min": 20,
          "max": 40
        }
      },
      "edges": {
        "font": {
          "size": 11,
          "face": "IBM Plex Mono",
          "color": "#4A625F"
        },
        "color": {
          "color": "#D5DFDB",
          "highlight": "#0B5F5B",
          "hover": "#2A9188"
        },
        "smooth": {
          "type": "continuous",
          "roundness": 0.5
        },
        "width": 2,
        "selectionWidth": 3
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "hideEdgesOnDrag": true,
        "navigationButtons": true,
        "keyboard": true
      },
      "layout": {
        "improvedLayout": true
      }
    }
    """)

    # Add nodes with styling
    for node_id in G.nodes():
        name = product_names.get(node_id, node_id)
        degree = G.degree(node_id)

        if node_id == selected_product_id:
            # Selected product - highlight prominently
            color = "#F2B233"  # Marigold
            border_color = "#15302E"
            size = 35
            border_width = 4
            label = f"★ {name}"
        elif node_id in reachable_set:
            # Reachable product - green/teal
            color = "#2A9188"  # Medium teal
            border_color = "#0B5F5B"
            size = 25 + min(degree * 2, 10)
            border_width = 3
            label = name
        else:
            # Unreachable product - muted
            color = "#E4ECE9"  # Track color
            border_color = "#9DB8B2"
            size = 20 + min(degree * 2, 8)
            border_width = 2
            label = name

        # Tooltip with details
        neighbors = list(G.neighbors(node_id))
        neighbor_names = [product_names.get(n, n) for n in neighbors]
        tooltip = (
            f"<b>{escape(name)}</b> ({escape(node_id)})<br>"
            f"Conexiones: {degree}<br>"
            f"Vecinos: {', '.join(neighbor_names) if neighbor_names else 'Ninguno'}"
        )

        net.add_node(
            node_id,
            label=label,
            title=tooltip,
            color=color,
            borderWidth=border_width,
            borderWidthSelected=border_width,
            size=size,
            font={"color": "#15302E" if node_id != selected_product_id else "#15302E"}
        )

    # Add edges with weight-based width
    for edge in G.edges(data=True):
        pid_a, pid_b, data = edge
        weight = data.get('weight', 0.5)
        # Edge width proportional to weight (2 to 6)
        width = 2 + weight * 4
        net.add_edge(
            pid_a,
            pid_b,
            value=width,
            title=f"Co-compra: {format_pct(weight)}",
            label=format_pct(weight),
            font={"size": 11, "face": "IBM Plex Mono", "color": "#4A625F"}
        )

    # Save to temporary file and render in Streamlit
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            net.save_graph(f.name)
            temp_path = f.name

        # Read the HTML and embed in Streamlit
        with open(temp_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Clean up temp file
        os.unlink(temp_path)

        # Render in Streamlit
        st.components.v1.html(html_content, height=620, scrolling=True)

    except Exception as e:
        st.error(f"Error al generar la visualización: {e}")
        # Fallback: show simple text representation
        _render_fallback(graph_data, selected_product_id, reachable_set)


def _render_fallback(graph_data, selected_product_id, reachable_set):
    """Fallback text-based visualization if PyVis fails."""
    st.subheader("Visualización de respaldo (texto)")

    products = graph_data.get('products', [])
    relationships = graph_data.get('relationships', [])

    # Build adjacency for display
    adj = {}
    for p in products:
        adj[p['id']] = {'name': p['name'], 'neighbors': []}

    for rel in relationships:
        a, b, w = rel['product_a'], rel['product_b'], rel['weight']
        adj[a]['neighbors'].append((b, w))
        adj[b]['neighbors'].append((a, w))

    # Show selected product and its connections
    if selected_product_id and selected_product_id in adj:
        sel = adj[selected_product_id]
        st.markdown(f"**Producto seleccionado:** ★ {sel['name']} ({selected_product_id})")
        if sel['neighbors']:
            st.markdown("**Conexiones directas:**")
            for nid, weight in sel['neighbors']:
                status = "✓ Alcanzable" if nid in reachable_set else "✗ No alcanzable"
                st.markdown(f"  - {adj[nid]['name']} ({nid}) — {format_pct(weight)} — {status}")
        else:
            st.markdown("*Sin conexiones directas*")

    # Show other products
    with st.expander("Ver todos los productos"):
        for pid, data in adj.items():
            if pid == selected_product_id:
                continue
            status = "✓ Alcanzable" if pid in reachable_set else "✗ No alcanzable"
            conn_count = len(data['neighbors'])
            st.markdown(f"- {data['name']} ({pid}) — {conn_count} conexiones — {status}")


def render_component_visualization(components_data):
    """
    Render a visualization of connected components (groups).

    Args:
        components_data: List of components from /components endpoint
    """
    if not components_data or not components_data.get('components'):
        st.info("No hay grupos para visualizar. Registre productos y relaciones primero.")
        return

    components = components_data['components']

    # Create a simplified view showing groups
    st.subheader("Grupos de productos conectados")

    for i, component in enumerate(components, 1):
        size = len(component)
        if size == 1:
            st.markdown(f"**Grupo {i}** — Producto aislado")
            p = component[0]
            st.markdown(f"  - {p['product_name']} ({p['product_id']}) — Sin relaciones")
        else:
            st.markdown(f"**Grupo {i}** — {size} productos conectados")
            for p in component:
                st.markdown(f"  - {p['product_name']} ({p['product_id']})")

    # Also show a simple network diagram for the largest component
    if components and len(components[0]) > 1:
        with st.expander("Ver diagrama del grupo principal"):
            largest = components[0]
            _render_simple_component_diagram(largest)


def _render_simple_component_diagram(component):
    """Render a simple text-based diagram for a component."""
    st.markdown("**Diagrama simplificado:**")
    for p in component:
        st.markdown(f"  • {p['product_name']} ({p['product_id']})")