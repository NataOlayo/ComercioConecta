"""
Piezas visuales reutilizables. Todo texto dinámico pasa por escape()
porque los nombres de producto los escribe el usuario.
"""
from html import escape

import streamlit as st

from frontend.utils.helpers import format_pct

STRONG = 0.7
MODERATE = 0.4


def strength_band(weight):
    """Devuelve el nombre de la banda de fuerza y su color (una sola gama, de claro a oscuro)."""
    if weight >= STRONG:
        return "Fuerte", "var(--cc-strong)"
    if weight >= MODERATE:
        return "Moderada", "var(--cc-medium)"
    return "Débil", "var(--cc-weak)"


def product_id(value):
    return f'<span class="cc-id">{escape(str(value))}</span>'


def tag(text, style="muted"):
    return f'<span class="cc-tag cc-tag-{style}">{escape(text)}</span>'


def strength(weight):
    name, color = strength_band(weight)
    return f'<span class="cc-strength"><span class="cc-dot" style="background:{color}"></span>{name}</span>'


def level_pips(weight):
    """Tres marcas que se llenan según la fuerza."""
    filled = {"Fuerte": 3, "Moderada": 2, "Débil": 1}[strength_band(weight)[0]]
    pips = "".join(f'<i class="{"on" if i < filled else ""}"></i>' for i in range(3))
    return f'<span class="cc-pips" aria-hidden="true">{pips}</span>'


def meter(weight):
    """Barra de 0 a 100 %."""
    _, color = strength_band(weight)
    label = format_pct(weight)
    return (
        f'<div class="cc-meter" role="img" aria-label="Fuerza {label}" title="{label}">'
        f'<span class="cc-meter-fill" style="width:{weight * 100:.1f}%;background:{color}"></span></div>'
    )


def path_chain(names, weights):
    """Dibuja el camino entre productos con el peso de cada tramo."""
    parts = []
    for index, name in enumerate(names):
        is_end = index == len(names) - 1
        parts.append(f'<span class="cc-node{" cc-node-end" if is_end else ""}">{escape(name)}</span>')
        if not is_end:
            parts.append(f'<span class="cc-edge"><small>{format_pct(weights[index])}</small></span>')
    return f'<div class="cc-chain">{"".join(parts)}</div>'


def table(columns, rows):
    """columns: lista de (título, es_numérica). rows: celdas ya escapadas."""
    head = "".join(f"<th>{escape(title)}</th>" for title, _ in columns)
    body = ""
    for row in rows:
        cells = "".join(
            f'<td{" class=num" if numeric else ""}>{cell}</td>'
            for (_, numeric), cell in zip(columns, row)
        )
        body += f"<tr>{cells}</tr>"
    return f'<div class="cc-table-wrap"><table class="cc-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render(content):
    st.html(content)


def page_header(title, lead):
    render(f'<header class="cc-page"><h1>{escape(title)}</h1><p>{escape(lead)}</p></header>')


def section(title, note=""):
    detail = f"<p>{escape(note)}</p>" if note else ""
    render(f'<div class="cc-section"><h2>{escape(title)}</h2>{detail}</div>')


def stats(items):
    """items: lista de (valor, etiqueta)."""
    blocks = "".join(
        f'<div class="cc-stat"><div class="cc-stat-value">{escape(str(value))}</div>'
        f'<div class="cc-stat-label">{escape(label)}</div></div>'
        for value, label in items
    )
    render(f'<div class="cc-stats">{blocks}</div>')


def empty_state(title, body):
    render(f'<div class="cc-empty"><h3>{escape(title)}</h3><p>{escape(body)}</p></div>')
