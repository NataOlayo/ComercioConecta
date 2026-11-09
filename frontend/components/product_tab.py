"""
Sección del analista para registrar y consultar productos
"""
from html import escape

import streamlit as st

from frontend.utils import ui
from frontend.utils.helpers import api_request, load_data


def render_product_tab():
    """Renderiza el catálogo y el formulario de productos"""
    ui.page_header("Productos", "Catálogo sintético que alimenta la red comercial.")

    products = st.session_state.get('products', [])
    connections = _connection_counts()
    isolated = sum(1 for p in products if not connections.get(p['id']))

    ui.stats([
        (len(products), "Productos registrados"),
        (len(products) - isolated, "Con relaciones"),
        (isolated, "Sin relaciones"),
    ])

    list_col, form_col = st.columns([3, 2], gap="large")
    with list_col:
        ui.section("Catálogo")
        if products:
            ui.render(_product_table(products, connections))
        else:
            ui.empty_state("Aún no hay productos", "Registre el primero con el formulario.")
    with form_col:
        ui.section("Agregar producto", "El código se genera automáticamente")
        _render_form(products)


def _connection_counts():
    counts = {}
    for relationship in st.session_state.get('relationships', []):
        for key in ('product_a', 'product_b'):
            counts[relationship[key]] = counts.get(relationship[key], 0) + 1
    return counts


def _product_table(products, connections):
    rows = []
    for product in products:
        count = connections.get(product['id'], 0)
        rows.append([
            ui.product_id(product['id']),
            f"<strong>{escape(product['name'])}</strong>",
            count,
            ui.tag("Conectado" if count else "Aislado", "outline" if count else "muted"),
        ])
    return ui.table([("Código", False), ("Producto", False), ("Conexiones", True), ("Situación", False)], rows)


def _render_form(products):
    with st.form("add_product_form", clear_on_submit=True, border=True):
        name = st.text_input("Nombre del producto", placeholder="Ej.: Yogur, Queso, Mermelada")
        submitted = st.form_submit_button("Agregar producto", type="primary", width="stretch")

    if not submitted:
        return

    name = name.strip()
    if not name:
        st.error("Escriba el nombre del producto.")
        return

    # El nombre se compara sin distinguir mayúsculas para evitar duplicados
    existing = next((p for p in products if p['name'].lower() == name.lower()), None)
    if existing:
        st.error(f"{existing['name']} ya está registrado con el código {existing['id']}.")
        return

    data, error = api_request("POST", "/products", {"name": name})
    if error:
        st.error(f"No se pudo agregar el producto: {error}")
        return

    st.toast(f"{name} agregado con el código {data['product']['id']}")
    load_data()
    st.rerun()
