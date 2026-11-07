"""Thème (clair / sombre), typographie et composants visuels de l'application."""
import html as _html

import streamlit as st

THEMES = {
    "light": dict(
        bg="#F6F3EC", bg2="#EFEBE1", surface="#FFFFFF", surface2="#FBF9F4",
        border="#E3DDD0", border_strong="#CFC7B6",
        ink="#15181C", ink2="#3C4148", muted="#767B82", faint="#A5A8AC",
        accent="#0B7A75", accent_ink="#FFFFFF", accent_soft="#E2F0EE", accent_line="#9ACFC9",
        warm="#F2DFC2", warm_ink="#7A4E17",
        danger="#A33A2B", danger_soft="#F7E4E0",
        grain="0.035", shadow="0 1px 0 rgba(21,24,28,.04), 0 12px 32px -18px rgba(21,24,28,.18)",
    ),
    "dark": dict(
        bg="#0D1012", bg2="#121619", surface="#161B1E", surface2="#1A2024",
        border="#252C31", border_strong="#334047",
        ink="#ECEAE4", ink2="#C3C6C6", muted="#8C9499", faint="#5E676D",
        accent="#46C2B8", accent_ink="#05201E", accent_soft="#123331", accent_line="#2A6E68",
        warm="#3A2D1C", warm_ink="#F0CD97",
        danger="#F08A79", danger_soft="#3A1D19",
        grain="0.05", shadow="0 1px 0 rgba(0,0,0,.4), 0 18px 40px -22px rgba(0,0,0,.8)",
    ),
}


def theme():
    return st.session_state.get("theme", "light")


def inject_css():
    t = THEMES[theme()]
    v = "\n".join(f"  --{k.replace('_', '-')}: {val};" for k, val in t.items())
    st.html(f"""<style>
@font-face {{ font-family: 'Instrument Serif'; font-style: normal; font-weight: 400; font-display: swap;
  src: url('app/static/instrument-serif-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; font-display: swap;
  src: url('app/static/instrument-serif-latin-400-italic.woff2') format('woff2'); }}
@font-face {{ font-family: 'Geist'; font-style: normal; font-weight: 100 900; font-display: swap;
  src: url('app/static/geist-latin-wght-normal.woff2') format('woff2-variations'); }}
@font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 400; font-display: swap;
  src: url('app/static/geist-mono-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 500; font-display: swap;
  src: url('app/static/geist-mono-latin-500-normal.woff2') format('woff2'); }}
:root {{
{v}
  --serif: 'Instrument Serif', Georgia, serif;
  --sans: 'Geist', 'Helvetica Neue', Helvetica, sans-serif;
  --mono: 'Geist Mono', ui-monospace, monospace;
  --r: 14px;
}}

/* ---------- Fond, texte, grain ---------- */
.stApp {{ background: var(--bg); color: var(--ink); font-family: var(--sans); }}
.stApp::before {{
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: var(--grain);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}}
.stApp p, .stApp li, .stApp label, .stApp button {{ font-family: var(--sans); }}
.stApp [data-testid="stIconMaterial"], .stApp .material-symbols-rounded {{ font-family: 'Material Symbols Rounded' !important; }}
.stApp p, .stApp li {{ color: var(--ink2); }}
[data-testid="stMainBlockContainer"] {{ max-width: 1120px; padding: 6.2rem 2rem 5rem; z-index: auto !important; }}
@media (max-width: 640px) {{ [data-testid="stMainBlockContainer"] {{ padding: 5.4rem 1rem 4rem; }} }}

/* ---------- Barre du haut ---------- */
[data-testid="stHeader"] {{ background: color-mix(in srgb, var(--bg) 82%, transparent); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border); }}
[data-testid="stDecoration"], [data-testid="stAppDeployButton"], [data-testid="stMainMenu"], #MainMenu,
[data-testid="stStatusWidget"] {{ display: none !important; }}
[data-testid="stHeader"] a, [data-testid="stHeader"] span, [data-testid="stHeader"] p {{
  font-family: var(--sans) !important; color: var(--muted); font-size: .9rem; }}
[data-testid="stHeader"] [data-testid="stTopNavLink"], [data-testid="stHeader"] [data-testid="stTopNavSection"] {{
  border-radius: 999px; }}
[data-testid="stHeader"] [data-testid="stTopNavLink"]:hover {{ background: var(--bg2); }}
[data-testid="stHeader"] [data-testid="stTopNavLink"][aria-current="page"] span,
[data-testid="stHeader"] a[aria-current="page"] span {{ color: var(--ink) !important; font-weight: 600; }}
[data-baseweb="popover"] [data-testid="stTopNavLink"] span {{ color: var(--ink2) !important; }}

/* ---------- Typographie ---------- */
.eyebrow {{ font-family: var(--mono); font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
  color: var(--muted); display: flex; gap: .7rem; align-items: center; flex-wrap: wrap; }}
.eyebrow .dot {{ width: 4px; height: 4px; border-radius: 50%; background: var(--faint); }}
.eyebrow .tag {{ color: var(--accent); }}
.display {{ font-family: var(--serif); font-weight: 400; color: var(--ink); letter-spacing: -.015em;
  line-height: .98; margin: .6rem 0 0; font-size: clamp(2.6rem, 6.4vw, 5.2rem); }}
.display em {{ font-style: italic; color: var(--accent); }}
.h2 {{ font-family: var(--serif); font-size: clamp(1.7rem, 3.4vw, 2.4rem); color: var(--ink); line-height: 1.05;
  margin: 0; letter-spacing: -.01em; }}
.lead {{ font-size: 1.08rem; line-height: 1.6; color: var(--ink2); max-width: 46rem; margin: 1.1rem 0 0; }}
.small {{ font-size: .86rem; color: var(--muted); line-height: 1.5; }}
.mono {{ font-family: var(--mono); }}
.rule {{ height: 1px; background: var(--border); margin: 2.4rem 0 2rem; border: 0; }}

/* ---------- Animation d'entrée ---------- */
@keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
.rise {{ animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}
.d1 {{ animation-delay: .06s; }} .d2 {{ animation-delay: .14s; }} .d3 {{ animation-delay: .22s; }} .d4 {{ animation-delay: .3s; }}
@media (prefers-reduced-motion: reduce) {{ .rise {{ animation: none; }} }}

/* ---------- Bandeau de statistiques ---------- */
.stats {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border); margin-top: 2.2rem; }}
.stat {{ padding: 1.1rem 1.2rem 1.15rem; border-left: 1px solid var(--border); }}
.stat:first-child {{ border-left: 0; padding-left: 0; }}
.stat .k {{ font-family: var(--mono); font-size: .68rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }}
.stat .v {{ font-family: var(--serif); font-size: 2rem; color: var(--ink); line-height: 1.1; margin-top: .3rem; }}
.stat .v small {{ font-family: var(--sans); font-size: .8rem; color: var(--muted); margin-left: .25rem; }}
@media (max-width: 760px) {{ .stats {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
  .stat:nth-child(3) {{ border-left: 0; padding-left: 0; border-top: 1px solid var(--border); }}
  .stat:nth-child(4) {{ border-top: 1px solid var(--border); }} }}

/* ---------- Cartes de l'accueil ---------- */
div[class*="st-key-card_"] {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--r);
  padding: 1.5rem 1.5rem 1.1rem; box-shadow: var(--shadow); transition: transform .25s ease, border-color .25s ease;
  height: 100%; animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}
div[class*="st-key-card_"]:hover {{ transform: translateY(-3px); border-color: var(--accent-line); }}
.card-top {{ display: flex; justify-content: space-between; align-items: baseline; }}
.card-num {{ font-family: var(--serif); font-size: 3rem; line-height: 1; color: var(--faint); }}
.pill {{ font-family: var(--mono); font-size: .66rem; letter-spacing: .1em; text-transform: uppercase;
  padding: .32rem .6rem; border-radius: 999px; border: 1px solid var(--border-strong); color: var(--ink2); }}
.pill.reg {{ background: var(--accent-soft); border-color: var(--accent-line); color: var(--accent); }}
.pill.clf {{ background: var(--warm); border-color: transparent; color: var(--warm-ink); }}
.card-title {{ font-family: var(--serif); font-size: 1.85rem; color: var(--ink); line-height: 1.05; margin: 1.6rem 0 .55rem; }}
.card-text {{ font-size: .93rem; color: var(--muted); line-height: 1.55; min-height: 4.6em; }}
.card-meta {{ display: flex; gap: 1.6rem; margin-top: 1.2rem; padding-top: 1rem; border-top: 1px dashed var(--border); }}
.card-meta div {{ font-family: var(--mono); font-size: .68rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }}
.card-meta b {{ display: block; font-family: var(--sans); font-size: .98rem; letter-spacing: 0; text-transform: none;
  color: var(--ink); font-weight: 600; margin-top: .15rem; }}

/* ---------- Liens de page ---------- */
[data-testid="stPageLink"] a {{ border-radius: 999px; padding: .2rem .2rem; }}
[data-testid="stPageLink"] a:hover {{ background: transparent; }}
[data-testid="stPageLink"] a p, [data-testid="stPageLink"] a span {{ color: var(--accent) !important; font-weight: 600; font-size: .92rem; }}
[data-testid="stPageLink"] a:hover p {{ text-decoration: underline; text-underline-offset: 4px; }}

/* ---------- Onglets ---------- */
[data-testid="stTabs"] [role="tablist"] {{ gap: 2rem; border-bottom: 1px solid var(--border); background: transparent; }}
[data-testid="stTab"] {{ background: transparent !important; padding: .75rem 0 !important; position: relative; }}
[data-testid="stTab"] p {{ font-size: .98rem !important; color: var(--muted) !important; font-weight: 500; transition: color .15s; }}
[data-testid="stTab"][data-selected="true"] p, [data-testid="stTab"]:hover p {{ color: var(--ink) !important; }}
[data-testid="stTabs"] .react-aria-SelectionIndicator {{ background: var(--accent) !important; height: 2px !important; }}
[data-testid="stTabs"] [role="tabpanel"] {{ padding-top: 2rem; }}
@media (max-width: 640px) {{ [data-testid="stTabs"] [role="tablist"] {{ gap: 1.1rem; }}
  [data-testid="stTab"] p {{ font-size: .88rem !important; }} }}

/* ---------- Formulaires et champs ---------- */
[data-testid="stForm"] {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--r);
  padding: 1.6rem 1.6rem 1.3rem; box-shadow: var(--shadow); }}
[data-testid="stWidgetLabel"] p {{ font-family: var(--mono); font-size: .7rem !important; letter-spacing: .1em;
  text-transform: uppercase; color: var(--muted) !important; }}
[data-testid="stSelectbox"] [role="group"], [data-testid="stNumberInputContainer"] {{
  background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important;
  transition: border-color .15s ease, box-shadow .15s ease; }}
[data-testid="stSelectbox"] [role="group"]:hover, [data-testid="stNumberInputContainer"]:hover {{ border-color: var(--border-strong) !important; }}
[data-testid="stSelectbox"] [role="group"]:focus-within, [data-testid="stNumberInputContainer"]:focus-within {{
  border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft); }}
[data-testid="stSelectbox"] input, [data-testid="stNumberInputField"] {{ background: transparent !important;
  color: var(--ink) !important; -webkit-text-fill-color: var(--ink); font-family: var(--sans) !important; font-size: .95rem !important; }}
[data-testid="stSelectbox"] button, [data-testid^="stNumberInputStep"] {{ background: transparent !important; border: 0 !important; }}
[data-testid="stSelectbox"] button svg, [data-testid^="stNumberInputStep"] svg {{ color: var(--muted) !important; fill: var(--muted) !important; }}
[data-testid^="stNumberInputStep"]:hover {{ background: var(--accent-soft) !important; }}
[data-testid^="stNumberInputStep"]:hover svg {{ color: var(--accent) !important; fill: var(--accent) !important; }}
[data-testid="stSelectboxVirtualDropdown"] {{ background: var(--surface) !important; border: 1px solid var(--border) !important;
  border-radius: 12px !important; box-shadow: var(--shadow) !important; overflow: hidden; }}
[data-testid="stSelectboxVirtualDropdown"] [role="option"] {{ color: var(--ink2) !important; font-family: var(--sans) !important;
  background: transparent !important; }}
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"] {{ background: var(--bg2) !important; color: var(--ink) !important; }}
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"] {{ background: var(--accent-soft) !important;
  color: var(--accent) !important; font-weight: 600; }}

/* ---------- Boutons ---------- */
.stApp button[kind^="primary"], .stApp [data-testid^="stBaseButton-primary"] {{
  background: var(--ink) !important; color: var(--bg) !important; border: 1px solid var(--ink) !important;
  border-radius: 999px !important; padding: .55rem 1.5rem !important; font-weight: 600; transition: transform .15s ease, background .2s; }}
.stApp [data-testid^="stBaseButton-primary"]:hover {{ background: var(--accent) !important; border-color: var(--accent) !important;
  color: var(--accent-ink) !important; transform: translateY(-1px); }}
.stApp [data-testid^="stBaseButton-primary"] p {{ color: inherit !important; font-weight: 600; }}
.stApp [data-testid^="stBaseButton-secondary"], [data-testid="stDownloadButton"] button {{
  background: transparent !important; color: var(--ink) !important; border: 1px solid var(--border-strong) !important;
  border-radius: 999px !important; padding: .5rem 1.2rem !important; }}
.stApp [data-testid^="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover {{
  border-color: var(--accent) !important; color: var(--accent) !important; }}
.stApp [data-testid^="stBaseButton-secondary"] p, [data-testid="stDownloadButton"] button p {{ color: inherit !important; }}

/* ---------- Sélecteur de thème ---------- */
.st-key-theme_switch {{ position: fixed !important; top: 13px; right: 22px; z-index: 1000002; width: auto !important; }}
.st-key-theme_switch [data-testid="stButtonGroup"] {{ justify-content: flex-end; }}
[data-testid="stTopNav"] {{ padding-right: 12rem; }}
.st-key-theme_switch button {{ border-radius: 999px !important; padding: .25rem .85rem !important; min-height: 0 !important;
  background: transparent !important; border: 1px solid var(--border) !important; }}
.st-key-theme_switch button p {{ font-family: var(--mono) !important; font-size: .7rem !important; letter-spacing: .1em;
  text-transform: uppercase; color: var(--muted) !important; }}
.st-key-theme_switch [role="radiogroup"] {{ gap: 0 !important; background: var(--bg2); border-radius: 999px; padding: 3px;
  border: 1px solid var(--border); }}
.st-key-theme_switch button {{ border: 0 !important; }}
.st-key-theme_switch button[data-selected="true"] {{ background: var(--surface) !important;
  box-shadow: 0 1px 2px rgba(0,0,0,.12), 0 0 0 1px var(--border); }}
.st-key-theme_switch button[data-selected="true"] p {{ color: var(--ink) !important; }}

/* ---------- Dépôt de fichier ---------- */
[data-testid="stFileUploaderDropzone"] {{ background: var(--surface) !important; border: 1.5px dashed var(--border-strong) !important;
  border-radius: var(--r) !important; padding: 1.6rem !important; }}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: var(--accent) !important; background: var(--accent-soft) !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] span, [data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzoneInstructions"] div {{ color: var(--muted) !important; }}
[data-testid="stFileUploaderDropzone"] svg {{ color: var(--accent); fill: var(--accent); }}
[data-testid="stFileUploaderDropzone"] {{ min-height: 128px; display: flex; align-items: center; gap: 1rem; }}
[data-testid="stFileUploaderDropzone"] button p {{ font-size: 0 !important; }}
[data-testid="stFileUploaderDropzone"] button p::after {{ content: "Choisir un fichier"; font-size: .9rem; }}
[data-testid="stFileUploaderDropzoneInstructions"] span {{ font-size: 0 !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] span::before {{ content: "ou glissez-déposez votre CSV ici"; display: block;
  font-size: .95rem; color: var(--ink2); }}
[data-testid="stFileUploaderDropzoneInstructions"] span::after {{ content: "Format CSV · 200 Mo maximum"; display: block;
  font-family: var(--mono); font-size: .66rem; letter-spacing: .1em; text-transform: uppercase; color: var(--faint); margin-top: .3rem; }}
[data-testid="stFileUploaderFile"] {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; }}
[data-testid="stFileUploaderFile"] * {{ color: var(--ink2) !important; }}
[data-testid="stFileChip"] {{ background: var(--surface2) !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important; }}
[data-testid="stFileChip"] *, [data-testid="stFileChipName"] {{ color: var(--ink) !important; }}
[data-testid="stFileChip"] small, [data-testid="stFileChip"] [data-testid="stIconMaterial"],
[data-testid="stFileUploader"] [data-testid^="stBaseButton-borderless"],
[data-testid="stFileUploader"] [data-testid^="stBaseButton-minimal"] {{ color: var(--muted) !important; }}
[data-testid="stFileChip"] svg {{ color: var(--accent) !important; }}

/* ---------- Résultat (lecture) ---------- */
.reading {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); box-shadow: var(--shadow);
  padding: 1.7rem 1.8rem 1.6rem; position: relative; overflow: hidden; height: 100%; }}
.reading::after {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--accent); }}
.reading .value {{ font-family: var(--serif); font-size: clamp(3.2rem, 7vw, 5.4rem); line-height: .95; color: var(--ink);
  margin: .9rem 0 .4rem; letter-spacing: -.02em; }}
.reading .value .u {{ font-size: .42em; color: var(--muted); margin-left: .2em; letter-spacing: 0; }}
.reading.empty .value {{ color: var(--faint); }}
.probs {{ margin-top: 1.3rem; display: grid; gap: .7rem; }}
.prob-row {{ display: grid; grid-template-columns: 8.5rem 1fr 3.4rem; gap: .8rem; align-items: center; }}
.prob-row .n {{ font-size: .9rem; color: var(--ink2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.prob-row .n.on {{ color: var(--ink); font-weight: 600; }}
.bar {{ height: 8px; border-radius: 999px; background: var(--bg2); overflow: hidden; }}
.bar i {{ display: block; height: 100%; border-radius: 999px; background: var(--border-strong); transform-origin: left;
  animation: grow .9s cubic-bezier(.2,.7,.2,1) both; }}
.bar i.on {{ background: var(--accent); }}
@keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
.prob-row .p {{ font-family: var(--mono); font-size: .8rem; color: var(--muted); text-align: right; }}
.recap {{ margin-top: 1.4rem; padding-top: 1rem; border-top: 1px dashed var(--border); display: flex; flex-wrap: wrap; gap: .45rem; }}
.chip {{ font-size: .78rem; padding: .28rem .6rem; border-radius: 8px; background: var(--bg2); color: var(--ink2); }}
.chip b {{ font-family: var(--mono); font-weight: 500; font-size: .66rem; text-transform: uppercase; letter-spacing: .08em;
  color: var(--muted); margin-right: .35rem; }}

/* ---------- Comparaison des algorithmes ---------- */
.cmp {{ display: grid; gap: 1rem; margin-top: 1.4rem; }}
.cmp-row {{ display: grid; grid-template-columns: 11rem 1fr 4rem; gap: 1rem; align-items: center; }}
.cmp-row .n {{ font-size: .95rem; color: var(--ink2); }}
.cmp-row.on .n {{ color: var(--ink); font-weight: 600; }}
.cmp-row .bar {{ height: 12px; }}
.cmp-row .p {{ font-family: var(--mono); font-size: .85rem; color: var(--muted); text-align: right; }}
.cmp-row.on .p {{ color: var(--accent); }}
@media (max-width: 640px) {{ .cmp-row, .prob-row {{ grid-template-columns: 7rem 1fr 3.2rem; gap: .6rem; }} }}

/* ---------- Tableaux ---------- */
.tbl-wrap {{ border: 1px solid var(--border); border-radius: var(--r); overflow: auto; max-height: 460px; background: var(--surface); }}
table.tbl {{ border-collapse: collapse; width: 100%; font-size: .86rem; }}
table.tbl th {{ position: sticky; top: 0; background: var(--surface2); text-align: left; font-family: var(--mono); font-weight: 500;
  font-size: .66rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); padding: .75rem .9rem;
  border-bottom: 1px solid var(--border); white-space: nowrap; }}
table.tbl td {{ padding: .62rem .9rem; border-bottom: 1px solid var(--border); color: var(--ink2); white-space: nowrap; }}
table.tbl tr:last-child td {{ border-bottom: 0; }}
table.tbl tr:hover td {{ background: var(--surface2); }}
table.tbl td.num {{ font-family: var(--mono); font-size: .8rem; text-align: right; }}
table.tbl th.pred, table.tbl td.pred {{ background: var(--accent-soft); color: var(--ink); font-weight: 600; }}
table.tbl th.pred {{ color: var(--accent); }}
table.tbl td.idx {{ font-family: var(--mono); font-size: .72rem; color: var(--faint); }}

/* ---------- Messages ---------- */
.note {{ display: flex; gap: .8rem; align-items: flex-start; padding: .9rem 1.1rem; border-radius: 12px; font-size: .9rem;
  line-height: 1.5; background: var(--bg2); color: var(--ink2); border: 1px solid var(--border); margin: .8rem 0; }}
.note::before {{ content: ""; flex: none; width: 6px; height: 6px; border-radius: 50%; background: var(--muted); margin-top: .5rem; }}
.note.err {{ background: var(--danger-soft); border-color: transparent; color: var(--danger); }}
.note.err::before {{ background: var(--danger); }}
.note.ok::before {{ background: var(--accent); }}
.cols-expected {{ display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .8rem; }}
.cols-expected span {{ font-family: var(--mono); font-size: .74rem; padding: .3rem .55rem; border-radius: 6px;
  border: 1px solid var(--border); color: var(--ink2); background: var(--surface); }}
.cols-expected span i {{ font-style: normal; color: var(--faint); margin-right: .35rem; }}

/* ---------- Pied de page ---------- */
.foot {{ margin-top: 4.5rem; padding-top: 1.4rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between;
  flex-wrap: wrap; gap: .8rem; font-family: var(--mono); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--faint); }}

/* ---------- Divers ---------- */
[data-testid="stCaptionContainer"] p {{ color: var(--muted) !important; }}
.stApp [data-testid="stSpinner"] * {{ color: var(--muted) !important; }}
[data-testid="stVerticalBlock"] {{ gap: 1rem; }}
</style>""")


# ---------------------------------------------------------------------------
# Formatage français
# ---------------------------------------------------------------------------
def fmt_num(x, decimals=0):
    s = f"{x:,.{decimals}f}".replace(",", "\u00a0").replace(".", ",")
    return s


def esc(x):
    return _html.escape(str(x))


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------
def theme_switch():
    """Sélecteur Clair / Sombre, aligné à droite en haut de chaque page."""
    if "theme_choice" not in st.session_state:
        st.session_state.theme_choice = "Sombre" if theme() == "dark" else "Clair"

    def on_change():
        v = st.session_state.theme_choice
        if v is None:  # clic sur l'option déjà active : on la garde sélectionnée
            st.session_state.theme_choice = "Sombre" if theme() == "dark" else "Clair"
        else:
            st.session_state.theme = "dark" if v == "Sombre" else "light"

    with st.container(key="theme_switch"):
        st.segmented_control("Thème", ["Clair", "Sombre"], label_visibility="collapsed",
                             key="theme_choice", on_change=on_change)


def stats(items):
    cells = "".join(f'<div class="stat"><div class="k">{esc(k)}</div><div class="v">{v}</div></div>' for k, v in items)
    st.html(f'<div class="stats rise d3">{cells}</div>')


def note(text, kind=""):
    st.html(f'<div class="note {kind}">{esc(text)}</div>')


def table(df, pred_col=None, max_rows=200):
    head = '<th></th>' + "".join(
        f'<th class="{"pred" if c == pred_col else ""}">{esc(c)}</th>' for c in df.columns)
    body = []
    for i, (_, row) in enumerate(df.head(max_rows).iterrows()):
        cells = [f'<td class="idx">{i + 1:02d}</td>']
        for c in df.columns:
            v = row[c]
            is_num = isinstance(v, (int, float)) and not isinstance(v, bool)
            if is_num:
                dec = 0 if float(v).is_integer() else 2
                txt = fmt_num(v, dec) if abs(v) >= 10000 else f"{v:.{dec}f}".replace(".", ",")
            else:
                txt = esc(v)
            cls = " ".join(x for x in ["num" if is_num else "", "pred" if c == pred_col else ""] if x)
            cells.append(f'<td class="{cls}">{txt}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    st.html(f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')
    if len(df) > max_rows:
        st.caption(f"Affichage des {max_rows} premières lignes sur {fmt_num(len(df))}. "
                   "Le fichier téléchargé contient toutes les lignes.")


def bars(rows, highlight, value_fmt, cls="cmp"):
    """rows: [(nom, valeur entre 0 et 1)]"""
    out = []
    for name, val in rows:
        on = name == highlight
        out.append(f'<div class="cmp-row {"on" if on else ""}"><div class="n">{esc(name)}</div>'
                   f'<div class="bar"><i class="{"on" if on else ""}" style="width:{max(val, 0) * 100:.1f}%"></i></div>'
                   f'<div class="p">{value_fmt(val)}</div></div>')
    return f'<div class="{cls}">{"".join(out)}</div>'


def footer():
    st.html('<div class="foot"><span>Devoir de Machine Learning · Licence 3</span>'
            '<span>Fatoumata Yarie Camara</span><span>scikit-learn · Streamlit</span></div>')
