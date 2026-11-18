"""
Main section for the sales clerk (encargado de ventas).
Shows store-language recommendations upfront; calculations in expandables.
Now includes graph visualization (Feature 4) in the right column.
"""
from html import escape

import streamlit as st

from frontend.components.product_picker import current_product, render_product_picker
from frontend.components.graph_visualization import render_graph_visualization
from frontend.utils import ui
from frontend.utils.helpers import api_request, format_pct, load_data

DEPTH_LABELS = {
    1: "Solo relaciones directas",
    2: "Hasta 2 pasos (recomendado)",
    3: "Hasta 3 pasos",
    4: "Hasta 4 pasos: cadenas largas",
}
UNREACHABLE_TAGS = {
    "otro_componente": "Otro grupo: sin relación demostrable",
    "fuera_del_alcance": "Mismo grupo, más allá de la profundidad",
}
DIRECT = "directa"
INDIRECT = "indirecta"


def render_exploration_tab():
    """Render recommendations for the selected product with graph visualization."""
    products = st.session_state.get('products', [])
    if not products:
        ui.page_header(
            "¿Qué le ofrezco al cliente?",
            "Elija lo que lleva el cliente y vea qué más le puede ofrecer."
        )
        ui.empty_state(
            "Aún no hay productos",
            "Registre productos y relaciones para recibir recomendaciones."
        )
        return

    ui.page_header(
        "¿Qué le ofrezco al cliente?",
        "Elija lo que lleva el cliente en su tiquete y vea qué más le puede ofrecer."
    )
    product_id = current_product(products, st.session_state.get('relationships', []))

    # Fetch recommendations
    data, error = api_request("GET", f"/recommendations/{product_id}")

    # Fetch graph data for visualization
    graph_data, _ = api_request("GET", "/graph/info")

    # Fetch reachability for highlighting
    reachability_data, _ = api_request("GET", f"/explore/reachability/{product_id}?depth=2")
    reachable_ids = []
    if reachability_data and not isinstance(reachability_data, dict):
        reachable_ids = [r['product_id'] for r in reachability_data.get('reachable', [])]

    # Layout: ticket on left, graph visualization on right (Feature 4)
    ticket_col, graph_col = st.columns([5, 4], gap="large")

    with ticket_col:
        # The selector is the "lleva" line of the ticket: a widget doesn't fit inside HTML,
        # so the container acts as paper and the ticket is built in three parts
        with st.container(key="cc_ticket"):
            ui.render(_ticket_head())
            render_product_picker(products, product_id)
            if error:
                st.error(f"No se pudieron generar las recomendaciones: {error}")
            else:
                ui.render(_ticket_body(data))

    with graph_col:
        # Feature 4: Graph visualization of connections
        ui.page_header(
            "Red de conexiones",
            f"Visualización interactiva desde {data.get('product_name', 'el producto seleccionado') if not error else 'el producto'}"
        )
        render_graph_visualization(
            graph_data,
            selected_product_id=product_id,
            reachable_products=reachable_ids,
            depth=2
        )

    if not error:
        with st.expander("Ver detalle técnico: cómo se calculó", icon=":material/calculate:"):
            _render_technical_detail(data)

    with st.expander("Análisis avanzado: BFS, DFS y alcanzabilidad", icon=":material/account_tree:"):
        _render_advanced_analysis(product_id)


RULE = '<hr class="cc-ticket-rule">'


def _ticket_head():
    return (
        '<div class="cc-ticket-flow"><div class="cc-ticket-head"><div class="cc-ticket-name">Tiquete del cliente</div>'
        '<div class="cc-ticket-sub">Datos sintéticos de demostración</div></div>' + RULE + '</div>'
    )


def _ticket_body(data):
    """What to offer the customer: direct, indirect, and what not to recommend."""
    direct = [p for p in data["proposals"] if p["type"] == DIRECT]
    indirect = [p for p in data["proposals"] if p["type"] == INDIRECT]

    sections = []
    if not data["proposals"]:
        sections.append(
            f'<div class="cc-ticket-group"><div class="cc-ticket-title"><h2>Por ahora no hay qué recomendar</h2></div>'
            f'<p class="cc-ticket-empty">{escape(_empty_reason(data))}</p></div>'
        )
    if direct:
        sections.append(_ticket_group("Ofrézcale", "Conexión directa", "solid", direct))
    if indirect:
        title = "También le puede interesar" if direct else "Ofrézcale"
        sections.append(_ticket_group(title, "Conexión indirecta", "outline", indirect))

    note = _unrelated_note(data)
    if note:
        sections.append(f'<p class="cc-ticket-foot">{escape(note)}</p>')

    return f'<div class="cc-ticket-flow">{RULE}{RULE.join(sections)}</div>'


def _ticket_group(title, connection, tag_style, proposals):
    lines = "".join(_ticket_line(proposal) for proposal in proposals)
    return (
        f'<div class="cc-ticket-group"><div class="cc-ticket-title"><h2>{escape(title)}</h2>'
        f'{ui.tag(connection, tag_style)}</div>{lines}</div>'
    )


def _ticket_line(proposal):
    level, _ = ui.strength_band(proposal["strength"])
    return (
        '<div class="cc-line"><div class="cc-line-main">'
        f'<strong>{escape(proposal["product_name"])}</strong><span class="cc-leader"></span>'
        f'{ui.level_pips(proposal["strength"])}<span class="cc-line-level">{level}</span></div>'
        f'<p>{escape(_plain_reason(proposal))}</p></div>'
    )


def _empty_reason(data):
    product = data["product_name"]
    if data["direct_connections"]:
        return f"{product} tiene relaciones, pero son muy débiles para recomendarlas con confianza."
    return f"Todavía no hay compras registradas que relacionen {product} con otros productos."


def _plain_reason(proposal):
    names = proposal["path_names"]
    if proposal["type"] == DIRECT:
        return f"Aparece en compras junto con {names[0]}."
    return f"{names[0]} se compra con {names[1]}, y {names[1]} se compra con {names[2]}."


def _unrelated_note(data):
    names = [e["product_name"] for e in data["excluded"] if e["reason_code"] == "otro_componente"]
    if not names:
        return ""

    product = data["product_name"]
    if len(names) == 1:
        return f"No se recomienda {names[0]}: no hay compras que lo relacionen con {product}."
    listed = ", ".join(names[:-1]) + f" y {names[-1]}"
    return f"No se recomiendan {listed}: no hay compras que los relacionen con {product}."


def _render_technical_detail(data):
    _render_rule_specs(data["rule"])
    if data["proposals"]:
        _render_proposals_table(data["proposals"])
    if data["direct_connections"]:
        _render_connections_table(data["direct_connections"])
    if data["excluded"]:
        _render_excluded_table(data["excluded"])


def _render_rule_specs(rule):
    specs = (
        ("Alcance", f"{rule['max_steps']} pasos"),
        ("Directa", f"≥ {format_pct(rule['min_direct'])}"),
        ("Indirecta", f"≥ {format_pct(rule['min_indirect'])}"),
        ("Máximo", f"{rule['limit']} productos"),
    )
    items = "".join(f'<span class="cc-spec">{name} <strong>{value}</strong></span>' for name, value in specs)
    ui.render(f'<div class="cc-specs cc-specs-start">{items}</div>')


def _render_proposals_table(proposals):
    ui.section("Productos recomendados", "Primero las conexiones directas, luego las indirectas; cada grupo por fuerza")
    ui.render(ui.table(
        [("#", True), ("Producto", False), ("Tipo", False), ("Fuerza", True), ("Camino y peso", False), ("Razón", False)],
        [
            [
                p["rank"],
                f"<strong>{escape(p['product_name'])}</strong> {ui.product_id(p['product_id'])}",
                escape(p["type"].capitalize()),
                format_pct(p["strength"]),
                ui.path_chain(p["path_names"], p["path_weights"]),
                escape(p["reason"]),
            ]
            for p in proposals
        ],
    ))


def _render_connections_table(connections):
    ui.section("Conexiones directas registradas")
    ui.render(ui.table(
        [("Producto", False), ("Co-compra", True), ("", False), ("Fuerza", False)],
        [
            [
                f"<strong>{escape(c['product_name'])}</strong> {ui.product_id(c['product_id'])}",
                format_pct(c["weight"]),
                ui.meter(c["weight"]),
                ui.strength(c["weight"]),
            ]
            for c in connections
        ],
    ))


def _render_excluded_table(excluded):
    ui.section("Productos descartados")
    ui.render(ui.table(
        [("Producto", False), ("Motivo", False)],
        [
            [f"<strong>{escape(item['product_name'])}</strong> {ui.product_id(item['product_id'])}",
             escape(item["reason"])]
            for item in excluded
        ],
    ))


def _render_advanced_analysis(product_id):
    depth_col, help_col = st.columns([3, 2])
    with depth_col:
        depth = st.slider("Número máximo de pasos", min_value=1, max_value=4, value=2)
    with help_col:
        ui.render(f'<div class="cc-specs">{ui.tag(DEPTH_LABELS[depth])}</div>')

    results = st.session_state.exploration_results
    actions = (("bfs", "Explorar con BFS"), ("dfs", "Explorar con DFS"), ("reachability", "Ver alcanzabilidad"))
    for column, (name, label) in zip(st.columns(3), actions):
        with column:
            if st.button(label, key=f"run_{name}", width="stretch"):
                data, error = api_request("GET", f"/explore/{name}/{product_id}?depth={depth}")
                if error:
                    st.error(f"Error: {error}")
                else:
                    results[name] = data
                    # Refresh to update graph visualization
                    load_data()
                    st.rerun()

    # Only show results for the selected product, not from a previous query
    for name, title in (("bfs", "BFS: exploración por niveles"), ("dfs", "DFS: exploración en profundidad")):
        data = results.get(name)
        if data and data["start_product"] == product_id:
            _render_traversal(title, data)

    reachability = results.get("reachability")
    if reachability and reachability["start_product_id"] == product_id:
        _render_reachability(reachability)


def _path_label(path):
    names = {p['id']: p['name'] for p in st.session_state.get('products', [])}
    return escape(" → ".join(names.get(product_id, product_id) for product_id in path))


def _traversal_table(items):
    return ui.table(
        [("Pasos", True), ("Producto", False), ("Peso acumulado", True), ("", False),
         ("Fuerza", False), ("Nivel", False), ("Camino", False)],
        [
            [
                item["distance"],
                f"<strong>{escape(item['product_name'])}</strong> {ui.product_id(item['product_id'])}",
                format_pct(item["cumulative_weight"]),
                ui.meter(item["cumulative_weight"]),
                ui.strength(item["cumulative_weight"]),
                escape(item["nivel_relacion"].capitalize()),
                _path_label(item["path"]),
            ]
            for item in items
        ],
    )


def _render_traversal(title, data):
    note = f"{data['results_count']} resultados · profundidad máxima {data['max_depth']}"
    if data["algorithm"] == "dfs":
        note += " · DFS muestra un producto una vez por cada camino"
    ui.section(title, note)

    if data["results_count"] == 0:
        ui.empty_state("Sin resultados", "No se encontraron productos relacionados con esta profundidad.")
        return
    ui.render(_traversal_table(data["results"]))


def _render_reachability(data):
    ui.section("Alcanzabilidad", f"Desde {data['start_product_name']} · profundidad máxima {data['max_depth']}")
    unreachable = data["unreachable"]
    ui.stats([
        (data["reachable_count"], "Alcanzables"),
        (sum(u["reason"] == "otro_componente" for u in unreachable), "En otro grupo"),
        (sum(u["reason"] == "fuera_del_alcance" for u in unreachable), "Fuera de alcance"),
    ])

    if data["reachable"]:
        ui.render(_traversal_table(data["reachable"]))
    if unreachable:
        ui.render(ui.table(
            [("Producto", False), ("Motivo", False)],
            [
                [f"<strong>{escape(u['product_name'])}</strong> {ui.product_id(u['product_id'])}",
                 escape(UNREACHABLE_TAGS[u["reason"]])]
                for u in unreachable
            ],
        ))