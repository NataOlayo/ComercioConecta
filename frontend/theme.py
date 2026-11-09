"""
Identidad visual de ComercioConecta: tienda de barrio (toldo y etiquetas de góndola).
Los colores de los controles nativos están en .streamlit/config.toml.
"""
import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
  --cc-surface: #FFFFFF;
  --cc-canvas: #F3F6F4;
  --cc-ink: #15302E;
  --cc-ink-2: #4A625F;
  --cc-ink-3: #5F7572;
  --cc-line: #D5DFDB;
  --cc-track: #E4ECE9;
  --cc-strong: #0B5F5B;
  --cc-medium: #2A9188;
  --cc-weak: #7DBDB4;
  --cc-marigold: #F2B233;
  --cc-sidebar: #0F3B3A;
  --cc-display: 'Bricolage Grotesque', 'Trebuchet MS', sans-serif;
  --cc-body: 'IBM Plex Sans', 'Segoe UI', sans-serif;
  --cc-mono: 'IBM Plex Mono', Consolas, monospace;
}

/* Animaciones: solo definen el inicio, así el estado final siempre es visible */
@keyframes cc-rise { from { opacity: 0; transform: translateY(16px); } }
.cc-page, .cc-stat, .cc-group, .cc-table-wrap, .cc-empty, .cc-prose, .cc-tech-grid {
  animation: cc-rise .55s cubic-bezier(.2, .7, .2, 1) both;
}
[data-testid="stSidebar"] .stButton button, .stButton button, [data-testid="stFormSubmitButton"] button {
  transition: background-color .18s ease, color .18s ease, transform .18s ease;
}
[data-testid="stSidebar"] .stButton button:hover { transform: translateX(3px); }

/* Marco general */
[data-testid="stMainBlockContainer"] { max-width: 1280px; padding: 2.25rem 2.5rem 4rem; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stHtml"] { font-family: var(--cc-body); color: var(--cc-ink); font-size: 15px; }
[data-testid="stHtml"] *, [data-testid="stHtml"] *::before { box-sizing: border-box; }

/* Toldo de la barra lateral */
[data-testid="stSidebar"]::before {
  content: ""; position: absolute; inset: 0 0 auto; height: 28px; z-index: 2; pointer-events: none;
  background:
    linear-gradient(90deg, var(--cc-marigold) 50%, #FFF8E8 50%) 0 0 / 36px 18px repeat-x,
    radial-gradient(circle at 9px 0, var(--cc-marigold) 9px, transparent 9.5px) 0 18px / 36px 10px repeat-x,
    radial-gradient(circle at 27px 0, #FFF8E8 9px, transparent 9.5px) 0 18px / 36px 10px repeat-x;
}
[data-testid="stSidebarHeader"] { padding-top: 2.5rem; height: auto; }
[data-testid="stSidebarUserContent"] { padding-top: 0; }
.cc-brand { padding: 0 2px 10px; }
.cc-brand-name { font: 700 25px/1.1 var(--cc-display); color: #FFFFFF; letter-spacing: -0.01em; }
.cc-brand-tag { font-size: 13px; color: #A9C7C2; margin-top: 4px; }
.cc-nav-label {
  font-size: 11.5px; font-weight: 600; letter-spacing: 0.09em; text-transform: uppercase;
  color: #8FB3AE; margin: 8px 2px -6px;
}
.cc-network { font-size: 13px; color: #A9C7C2; border-top: 1px solid #27605D; padding-top: 12px; margin-top: 8px; line-height: 1.7; }
.cc-network strong { color: #FFFFFF; font-weight: 600; font-variant-numeric: tabular-nums; }

/* Navegación */
[data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] { gap: 0.2rem; }
[data-testid="stSidebar"] .cc-nav-label { margin: 14px 2px 4px; }
[data-testid="stSidebar"] .stButton button { justify-content: flex-start; min-height: 40px; padding: 0 12px; border: 0; }
[data-testid="stSidebar"] .stButton button div { justify-content: flex-start; }
[data-testid="stSidebar"] .stButton button p { font-size: 14.5px; font-weight: 500; }
[data-testid="stSidebar"] [data-testid="stBaseButton-tertiary"] { color: #D5E5E2; width: 100%; }
[data-testid="stSidebar"] [data-testid="stBaseButton-tertiary"]:hover { background: #1A4E4C; color: #FFFFFF; }
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] { background: var(--cc-marigold); color: #15302E; }
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover { background: #F7C25A; color: #15302E; }
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p,
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] span { color: #15302E; }

/* Controles */
[data-testid="stExpander"] details { background: var(--cc-surface); border-color: var(--cc-line); }
[data-testid="stExpander"] summary p { font-weight: 600; }
[data-testid="stForm"] { background: var(--cc-surface); border-color: var(--cc-line); padding: 1.25rem; }

/* Encabezados */
.cc-page h1 { font: 700 34px/1.1 var(--cc-display); letter-spacing: -0.02em; margin: 0; padding: 0; color: var(--cc-ink); text-wrap: balance; }
.cc-page p { margin: 8px 0 0; color: var(--cc-ink-2); font-size: 16px; max-width: 68ch; }
.cc-section { display: flex; flex-direction: column; gap: 2px; }
.cc-section h2 { font: 650 19px/1.25 var(--cc-display); margin: 0; padding: 0; color: var(--cc-ink); }
.cc-section p { margin: 0; font-size: 13.5px; color: var(--cc-ink-3); }

/* Resumen numérico */
.cc-stats { display: flex; flex-wrap: wrap; border-block: 1px solid var(--cc-line); padding-block: 14px; row-gap: 12px; }
.cc-stat { flex: 1 1 130px; padding-inline: 20px; border-left: 1px solid var(--cc-line); min-width: 0; }
.cc-stat:first-child { padding-left: 0; border-left: 0; }
.cc-stat-value { font: 650 30px/1.1 var(--cc-display); font-variant-numeric: tabular-nums; color: var(--cc-ink); }
.cc-stat-label { font-size: 13px; color: var(--cc-ink-3); margin-top: 2px; }

/* Etiquetas */
.cc-id { font: 500 12px/1 var(--cc-mono); color: var(--cc-ink-2); background: var(--cc-track); padding: 3px 6px; border-radius: 3px; white-space: nowrap; }
.cc-tag { display: inline-block; font-size: 12px; font-weight: 600; line-height: 1; padding: 5px 8px; border-radius: 4px; white-space: nowrap; }
.cc-tag-solid { background: var(--cc-strong); color: #FFFFFF; }
.cc-tag-outline { color: var(--cc-strong); box-shadow: inset 0 0 0 1.5px var(--cc-strong); border-radius: 4px; }
.cc-tag-muted { background: var(--cc-track); color: var(--cc-ink-2); }
.cc-strength { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: var(--cc-ink-2); white-space: nowrap; }
.cc-dot { width: 9px; height: 9px; border-radius: 50%; flex: none; }
.cc-specs { display: flex; flex-wrap: wrap; gap: 8px 22px; justify-content: flex-end; padding-top: 30px; }
.cc-specs-start { justify-content: flex-start; padding-top: 0; }
.cc-spec { font-size: 13px; color: var(--cc-ink-3); white-space: nowrap; }
.cc-spec strong { color: var(--cc-ink); font-weight: 600; font-variant-numeric: tabular-nums; }

/* Barra de fuerza */
.cc-meter { position: relative; height: 8px; background: var(--cc-track); border-radius: 4px; min-width: 60px; }
.cc-meter-fill { position: absolute; inset: 0 auto 0 0; border-radius: 4px; }

/* Tiquete de tienda con la respuesta al encargado */
/* El contenedor es el papel del tiquete; el borde dentado de abajo es el ::after */
.st-key-cc_ticket {
  position: relative; max-width: 520px; gap: 14px; margin-bottom: 14px;
  background: var(--cc-surface); border-top: 6px solid var(--cc-marigold); padding: 28px 28px 22px;
  filter: drop-shadow(0 12px 18px rgba(15, 59, 58, .18));
  animation: cc-rise .55s cubic-bezier(.2, .7, .2, 1) both;
}
.st-key-cc_ticket::after {
  content: ""; position: absolute; left: 0; right: 0; top: 100%; height: 10px;
  background: radial-gradient(circle at 8px 10px, transparent 7px, var(--cc-surface) 7.5px) 0 0 / 16px 10px repeat-x;
}
.cc-ticket-flow { display: flex; flex-direction: column; gap: 14px; }
.cc-ticket-head { text-align: center; }
.cc-ticket-name { font: 700 20px/1.2 var(--cc-display); letter-spacing: .02em; text-transform: uppercase; }
.cc-ticket-sub { font: 400 12.5px/1.4 var(--cc-mono); color: var(--cc-ink-2); margin-top: 2px; }
.cc-ticket-rule { border: 0; border-top: 2px dashed #9DB8B2; margin: 0; }

/* Selector del producto: la línea "lleva" del tiquete */
.cc-pick-label { font: 600 12.5px/1.2 var(--cc-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--cc-strong); }
.st-key-cc_picker button { width: 100%; justify-content: space-between; min-height: 60px; padding: 8px 14px; background: #FFFBF0; border: 1.5px solid var(--cc-strong); border-radius: 12px; transition: box-shadow .15s ease; }
.st-key-cc_picker button, .st-key-cc_picker button:active, .st-key-cc_picker button[aria-expanded="true"] { background: #FFFBF0; border-color: var(--cc-strong); }
.st-key-cc_picker button:hover, .st-key-cc_picker button:focus-visible, .st-key-cc_picker button[aria-expanded="true"] { box-shadow: 0 0 0 4px rgba(11, 95, 91, .14); }
.st-key-cc_picker button > div { display: flex; align-items: center; justify-content: space-between; width: 100%; }
.st-key-cc_picker button > div > div:first-child { flex: 1; justify-content: flex-start; text-align: left; }
/* La flecha del campo va dentro de un círculo amarillo */
.st-key-cc_picker button > div > div[aria-hidden="true"] { display: grid; place-items: center; flex: none; width: 32px; height: 32px; border-radius: 50%; background: var(--cc-marigold); color: var(--cc-ink); }
.st-key-cc_picker button p { font: 700 23px/1.1 var(--cc-display); color: var(--cc-ink); }
.st-key-cc_picker button p span { font: 500 13px/1.1 var(--cc-body); }
[data-testid="stPopoverBody"] { width: min(464px, 92vw); padding: 0; border: 1px solid var(--cc-line); border-radius: 16px; box-shadow: 0 24px 40px -12px rgba(15, 59, 58, .45); background: var(--cc-surface); overflow-y: auto; overscroll-behavior: contain; }
/* Filas más juntas y un respiro al final para que la última no quede cortada */
[data-testid="stPopoverBody"] > [data-testid="stVerticalBlock"] { gap: 2px; padding: 8px 8px 14px; }
.cc-pick-group { display: flex; align-items: center; gap: 10px; padding: 8px 4px 0; font: 600 11.5px/1 var(--cc-body); letter-spacing: .09em; text-transform: uppercase; color: var(--cc-ink-3); }
.cc-pick-group::after { content: ""; flex: 1; border-top: 1px dashed #B9CBC5; }
[data-testid="stPopoverBody"] button { justify-content: flex-start; min-height: 44px; padding: 0 12px; border: 0; border-radius: 10px; }
[data-testid="stPopoverBody"] button > div { width: 100%; justify-content: flex-start; }
[data-testid="stPopoverBody"] button p { font-size: 16px; font-weight: 600; color: var(--cc-ink); }
[data-testid="stPopoverBody"] button p span { font-size: 12.5px; font-weight: 400; }
[data-testid="stPopoverBody"] [data-testid="stBaseButton-tertiary"]:hover { background: #E9F1EE; }
[data-testid="stPopoverBody"] [data-testid="stBaseButton-primary"] { background: #FFF3D6; }
[data-testid="stPopoverBody"] [data-testid="stBaseButton-primary"] [data-testid="stIconMaterial"] { color: var(--cc-strong); }
.cc-ticket-group { display: flex; flex-direction: column; gap: 14px; }
.cc-ticket-title { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.cc-ticket-title h2 { font: 700 19px/1.25 var(--cc-display); margin: 0; padding: 0; color: var(--cc-ink); }
.cc-ticket-empty { margin: 0; color: var(--cc-ink-2); line-height: 1.5; }
.cc-line { display: flex; flex-direction: column; gap: 4px; }
.cc-line-main { display: flex; align-items: baseline; gap: 8px; }
.cc-line-main strong { font: 700 22px/1.15 var(--cc-display); color: var(--cc-ink); overflow-wrap: anywhere; }
.cc-leader { flex: 1; min-width: 12px; border-bottom: 2px dotted #9DB8B2; }
.cc-line-main .cc-pips { align-self: center; }
.cc-line-level { min-width: 64px; text-align: right; font-size: 13px; font-weight: 600; color: var(--cc-strong); }
.cc-line p { margin: 0; font-size: 14px; line-height: 1.45; color: var(--cc-ink-2); }
.cc-ticket-foot { margin: 0; font: 400 12.5px/1.5 var(--cc-mono); color: var(--cc-ink-2); }
.cc-pips { display: inline-flex; gap: 3px; }
.cc-pips i { width: 15px; height: 6px; border-radius: 3px; background: var(--cc-track); }
.cc-pips i.on { background: var(--cc-marigold); }

/* Camino en el detalle técnico */
.cc-chain { display: flex; align-items: center; }
.cc-node { font-size: 13px; font-weight: 500; padding: 4px 9px; border-radius: 4px; background: var(--cc-track); color: var(--cc-ink); white-space: nowrap; }
.cc-node-end { background: var(--cc-strong); color: #FFFFFF; }
.cc-edge { display: inline-flex; flex-direction: column; align-items: center; min-width: 52px; padding-inline: 4px; }
.cc-edge small { font: 500 11.5px/1.2 var(--cc-mono); color: var(--cc-ink-2); }
.cc-edge::after { content: ""; display: block; width: 100%; border-top: 2px solid var(--cc-ink-3); }

/* Tablas */
.cc-table-wrap { overflow-x: auto; background: var(--cc-surface); border: 1px solid var(--cc-line); border-radius: 8px; }
.cc-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.cc-table th { text-align: left; font-size: 12px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: var(--cc-ink-3); padding: 12px 16px; border-bottom: 1px solid var(--cc-line); white-space: nowrap; }
.cc-table td { padding: 11px 16px; border-bottom: 1px solid var(--cc-track); vertical-align: middle; }
.cc-table tr:last-child td { border-bottom: 0; }
.cc-table tbody tr { transition: background-color .15s ease; }
.cc-table tbody tr:hover { background: var(--cc-canvas); }
.cc-table td.num { font-variant-numeric: tabular-nums; font-weight: 600; }
.cc-table .cc-meter { width: 120px; }

/* Estado vacío */
.cc-empty { background: var(--cc-surface); border: 1px dashed #A9BAB5; border-radius: 8px; padding: 26px 24px; }
.cc-empty h3 { font: 650 18px/1.25 var(--cc-display); margin: 0 0 6px; padding: 0; color: var(--cc-ink); }
.cc-empty p { margin: 0; color: var(--cc-ink-2); max-width: 62ch; }

/* Grupos */
.cc-groups { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 14px; }
.cc-group { background: var(--cc-surface); border: 1px solid var(--cc-line); border-radius: 14px; padding: 18px 20px; display: flex; flex-direction: column; gap: 12px; transition: transform .22s ease, box-shadow .22s ease; }
.cc-group:hover { transform: translateY(-4px); box-shadow: 0 14px 28px -14px rgba(15, 59, 58, .45); }
.cc-group-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.cc-group-head h3 { font: 650 18px/1.2 var(--cc-display); margin: 0; padding: 0; color: var(--cc-ink); }
.cc-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.cc-chip { display: inline-flex; align-items: center; gap: 6px; font-size: 13.5px; font-weight: 500; background: var(--cc-canvas); padding: 5px 8px; border-radius: 4px; }
.cc-group-note { margin: 0; font-size: 13px; color: var(--cc-ink-3); }

/* Texto explicativo */
.cc-prose { display: flex; flex-direction: column; gap: 10px; }
.cc-prose h2 { font: 650 21px/1.25 var(--cc-display); margin: 12px 0 0; padding: 0; color: var(--cc-ink); }
.cc-prose p, .cc-prose li { color: var(--cc-ink-2); line-height: 1.6; max-width: 70ch; }
.cc-prose p { margin: 0; }
.cc-prose ul { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; }
.cc-prose strong { color: var(--cc-ink); }

/* Análisis técnico: una tarjeta por punto que se explica en el pitch */
.cc-tech-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.cc-tech-card { background: var(--cc-canvas); border-radius: 10px; padding: 18px 20px; display: flex; flex-direction: column; gap: 8px; }
.cc-tech-card h3 { font: 600 12px/1.2 var(--cc-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--cc-strong); margin: 0; padding: 0; }
.cc-tech-card p, .cc-tech-card li { margin: 0; font-size: 14.5px; line-height: 1.5; color: var(--cc-ink-2); }
.cc-tech-card ul { margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 4px; }
.cc-tech-card strong { color: var(--cc-ink); }
.cc-code { font: 400 13px/1.55 var(--cc-mono); background: var(--cc-surface); border: 1px solid var(--cc-line); border-radius: 6px; padding: 8px 10px; color: var(--cc-ink); }

@media (prefers-reduced-motion: reduce) {
  [data-testid="stAppViewContainer"] *, [data-testid="stSidebar"] * { animation: none !important; transition: none !important; }
}

@media (max-width: 640px) {
  .st-key-cc_ticket { padding: 22px 18px 18px; }
  [data-testid="stMainBlockContainer"] { padding: 3.5rem 1rem 3rem; }
  .cc-page h1 { font-size: 28px; }
  .cc-specs { justify-content: flex-start; padding-top: 0; }
  .cc-stat { flex-basis: 40%; }
  .cc-stat:nth-child(odd) { padding-left: 0; border-left: 0; }
}
"""


def apply_theme() -> None:
    """Inyecta la hoja de estilos de la aplicación."""
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
