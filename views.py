"""Pages de l'application : accueil et page de chaque modèle."""
import io

import pandas as pd
import streamlit as st

import models as M
import ui
from ui import esc, fmt_num

PAGES = {}  # rempli par Accueil.py (objets st.Page)

METHOD = {
    "taxi": "RobustScaler",
    "car_dataset": "RobustScaler",
    "telephone": "MinMaxScaler",
    "car_data": "MinMaxScaler",
}


def _title_html(title):
    words = title.split(" ")
    return esc(" ".join(words[:-1])) + " <em>" + esc(words[-1]) + "</em>"


def _metric_txt(cfg, v=None):
    v = cfg["metric"] if v is None else v
    return fmt_num(v, 3)


def _display_value(f, v):
    return M.FR.get(v, v) if f["kind"] == "cat" else v


# ===========================================================================
# Accueil
# ===========================================================================
def home():
    st.html("""
<div class="rise"><div class="eyebrow"><span class="tag">Atelier de prédiction</span><span class="dot"></span>
<span>Quatre modèles</span><span class="dot"></span><span>Régression et classification</span></div></div>
<h1 class="display rise d1">Quatre modèles,<br><em>une seule application.</em></h1>
<p class="lead rise d2">Des modèles de machine learning entraînés sur des données réelles : courses de taxi,
téléphones et voitures vendus à Dakar, voitures d'occasion. Choisissez un modèle, remplissez le formulaire
pour une prédiction immédiate, ou déposez un fichier CSV pour en traiter des milliers d'un coup.</p>""")
    total = sum(c["rows"] for c in M.MODELS.values())
    ui.stats([("Modèles", "4"), ("Observations", fmt_num(total)),
              ("Régressions", "2"), ("Classifications", "2")])

    st.html('<div style="height:2.6rem"></div><div class="eyebrow"><span>Les modèles</span></div>')
    keys = list(M.MODELS)
    for row in (keys[:2], keys[2:]):
        cols = st.columns(2, gap="medium")
        for col, key in zip(cols, row):
            cfg = M.MODELS[key]
            reg = cfg["kind"] == "regression"
            with col:
                with st.container(key=f"card_{key}"):
                    st.html(f"""
<div class="card-top"><span class="card-num">{cfg['number']}</span>
<span class="pill {'reg' if reg else 'clf'}">{'Régression' if reg else 'Classification'}</span></div>
<div class="card-title">{esc(cfg['title'])}</div>
<div class="card-text">{esc(cfg['lead'])}</div>
<div class="card-meta"><div>Algorithme<b>{esc(cfg['algo'])}</b></div>
<div>{esc(cfg['metric_name'])}<b>{_metric_txt(cfg)}</b></div>
<div>Données<b>{fmt_num(cfg['rows'])}</b></div></div>""")
                    st.page_link(PAGES[key], label="Ouvrir le modèle  →")
    ui.footer()


# ===========================================================================
# Page d'un modèle
# ===========================================================================
def make_model_page(key):
    def render():
        model_page(key)
    render.__name__ = f"page_{key}"
    return render


def model_page(key):
    cfg = M.MODELS[key]
    reg = cfg["kind"] == "regression"
    obj = M.load(key)

    st.html(f"""
<div class="rise"><div class="eyebrow"><span class="tag">Modèle {cfg['number']}</span><span class="dot"></span>
<span>{'Régression' if reg else 'Classification'}</span><span class="dot"></span><span>{esc(cfg['algo'])}</span></div></div>
<h1 class="display rise d1">{_title_html(cfg['title'])}</h1>
<p class="lead rise d2">{esc(cfg['lead'])}</p>""")
    ui.stats([
        ("Algorithme", esc(cfg["algo"])),
        (f"{cfg['metric_name']} validation", _metric_txt(cfg)),
        ("Observations", fmt_num(cfg["rows"])),
        ("Variables", str(len(cfg["features"]))),
    ])
    st.html('<div style="height:2rem"></div>')

    t1, t2, t3 = st.tabs(["Prédiction simple", "Prédiction multiple", "Le modèle"])
    with t1:
        single_tab(key, cfg, obj, reg)
    with t2:
        batch_tab(key, cfg, reg)
    with t3:
        about_tab(key, cfg, reg)
    ui.footer()


# ---------------------------------------------------------------------------
# Prédiction simple
# ---------------------------------------------------------------------------
def single_tab(key, cfg, obj, reg):
    left, right = st.columns([1.2, 1], gap="large")
    with left:
        with st.form(f"form_{key}", border=False):
            values = {}
            feats = cfg["features"]
            half = (len(feats) + 1) // 2
            c1, c2 = st.columns(2, gap="medium")
            for i, f in enumerate(feats):
                with (c1 if i < half else c2):
                    if f["kind"] == "cat":
                        opts = obj["uniques"][f["index"]]
                        values[f["name"]] = st.selectbox(
                            f["label"], opts, format_func=lambda v: M.FR.get(v, v), key=f"in_{key}_{f['name']}")
                    else:
                        is_int = isinstance(f["default"], int)
                        cast = int if is_int else float
                        values[f["name"]] = st.number_input(
                            f["label"],
                            min_value=None if f["min"] is None else cast(f["min"]),
                            max_value=None if f["max"] is None else cast(f["max"]),
                            value=cast(f["default"]), step=cast(f["step"]),
                            format="%d" if is_int else "%.2f", key=f"in_{key}_{f['name']}")
            st.html('<div style="height:.4rem"></div>')
            submitted = st.form_submit_button("Lancer la prédiction", type="primary")
        if submitted:
            df = pd.DataFrame([values])[M.feature_names(key)]
            preds, probs, classes = M.predict(key, df)
            st.session_state[f"res_{key}"] = dict(
                pred=preds[0], probs=None if probs is None else probs[0].tolist(), classes=classes, inputs=values)

    with right:
        res = st.session_state.get(f"res_{key}")
        st.html(reading_html(cfg, reg, res))


def reading_html(cfg, reg, res):
    head = (f'<div class="eyebrow"><span class="tag">{esc(cfg["target_label"])}</span>'
            f'<span class="dot"></span><span>{esc(cfg["algo"])}</span></div>')
    if res is None:
        return (f'<div class="reading empty">{head}<div class="value">—</div>'
                f'<p class="small">Renseignez les caractéristiques puis lancez la prédiction. '
                f'Le résultat apparaîtra ici.</p></div>')
    if reg:
        unit = f'<span class="u">{esc(cfg["unit"])}</span>' if cfg.get("unit") else ""
        body = f'<div class="value rise">{fmt_num(res["pred"], cfg["decimals"])}{unit}</div>'
        sub = cfg.get("unit_note") or f'{cfg["metric_name"]} de {_metric_txt(cfg)} sur les données de validation.'
        body += f'<p class="small">{esc(sub)}</p>'
    else:
        probs = sorted(zip(res["classes"], res["probs"]), key=lambda x: -x[1])
        body = f'<div class="value rise">{esc(res["pred"])}</div>'
        body += f'<p class="small">Confiance du modèle : <b>{fmt_num(probs[0][1] * 100)} %</b></p>'
        rows = "".join(
            f'<div class="prob-row"><div class="n {"on" if c == res["pred"] else ""}">{esc(c)}</div>'
            f'<div class="bar"><i class="{"on" if c == res["pred"] else ""}" style="width:{p * 100:.1f}%"></i></div>'
            f'<div class="p">{fmt_num(p * 100)} %</div></div>' for c, p in probs)
        body += f'<div class="probs">{rows}</div>'
    chips = "".join(
        f'<span class="chip"><b>{esc(f["label"])}</b>'
        f'{esc(_fmt_input(f, res["inputs"][f["name"]]))}</span>' for f in cfg["features"])
    return f'<div class="reading">{head}{body}<div class="recap">{chips}</div></div>'


def _fmt_input(f, v):
    if f["kind"] == "cat":
        return M.FR.get(v, v)
    return fmt_num(v, 0 if float(v).is_integer() else 2)


# ---------------------------------------------------------------------------
# Prédiction multiple
# ---------------------------------------------------------------------------
def batch_tab(key, cfg, reg):
    names = M.feature_names(key)
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        st.html(f"""<div class="h2">Traiter un fichier entier</div>
<p class="small" style="margin-top:.8rem;font-size:.95rem">Déposez un CSV contenant les {len(names)} variables
ci-dessous. Les colonnes sont reconnues par leur nom ; à défaut, elles sont lues dans cet ordre.
Les colonnes supplémentaires, comme la vraie valeur, sont conservées dans le résultat.</p>
<div class="cols-expected">{''.join(f'<span><i>{i + 1:02d}</i>{esc(n)}</span>' for i, n in enumerate(names))}</div>""")
        st.html('<div style="height:.4rem"></div>')
        with open(f"{cfg['folder']}/sample_df.csv", "rb") as fh:
            st.download_button("Télécharger un fichier d'exemple", fh.read(),
                               file_name=f"exemple_{key}.csv", mime="text/csv", key=f"tpl_{key}")
    with right:
        file = st.file_uploader("Fichier CSV", type=["csv"], key=f"up_{key}", label_visibility="collapsed")

    if file is None:
        st.session_state.pop(f"batch_{key}", None)
        return

    try:
        raw = pd.read_csv(io.BytesIO(file.getvalue()))
    except Exception:
        ui.note("Impossible de lire ce fichier. Vérifiez qu'il s'agit bien d'un CSV séparé par des virgules.", "err")
        return

    X, notes, error = M.prepare_csv(key, raw)
    st.html('<div class="rule"></div>')
    if error:
        ui.note(error, "err")
        return

    head_l, head_r = st.columns([3, 1], vertical_alignment="bottom")
    with head_l:
        st.html(f'<div class="eyebrow"><span>Aperçu</span><span class="dot"></span>'
                f'<span>{fmt_num(len(raw))} ligne(s)</span><span class="dot"></span><span>{esc(notes[0])}</span></div>')
    with head_r:
        run = st.button("Lancer les prédictions", type="primary", key=f"run_{key}", width="stretch")

    sig = (file.file_id if hasattr(file, "file_id") else file.name, len(raw))
    if run:
        preds, probs, _ = M.predict(key, X)
        out = raw.copy()
        col = f"{cfg['target']}_Prediction"
        out[col] = preds
        if probs is not None:
            out["Confiance_%"] = (probs.max(axis=1) * 100).round(1)
        st.session_state[f"batch_{key}"] = dict(sig=sig, df=out, col=col)

    res = st.session_state.get(f"batch_{key}")
    if res is None or res["sig"] != sig:
        ui.table(raw.head(10))
        return

    out, col = res["df"], res["col"]
    if reg:
        p = out[col]
        unit = f" {cfg['unit']}" if cfg.get("unit") else ""
        items = [("Lignes prédites", fmt_num(len(out))),
                 ("Moyenne", fmt_num(p.mean(), 2) + f"<small>{esc(unit)}</small>"),
                 ("Minimum", fmt_num(p.min(), 2) + f"<small>{esc(unit)}</small>"),
                 ("Maximum", fmt_num(p.max(), 2) + f"<small>{esc(unit)}</small>")]
        if cfg["target"] in out.columns and pd.api.types.is_numeric_dtype(out[cfg["target"]]):
            err = (out[cfg["target"]] - p).abs().mean()
            items[3] = ("Écart moyen au réel", fmt_num(err, 2) + f"<small>{esc(unit)}</small>")
    else:
        counts = out[col].value_counts()
        items = [("Lignes prédites", fmt_num(len(out)))]
        items += [(c, f"{fmt_num(n)}<small>{fmt_num(n / len(out) * 100)} %</small>") for c, n in counts.head(2).items()]
        if cfg["target"] in out.columns:
            acc = (out[cfg["target"]].astype(str) == out[col].astype(str)).mean()
            items.append(("Concordance avec le réel", f"{fmt_num(acc * 100)}<small>%</small>"))
        else:
            items.append(("Confiance moyenne", f"{fmt_num(out['Confiance_%'].mean())}<small>%</small>"))
    ui.stats(items[:4])
    st.html('<div style="height:1.4rem"></div>')
    ui.table(out, pred_col=col)
    st.html('<div style="height:.6rem"></div>')
    st.download_button("Télécharger les prédictions (CSV)", out.to_csv(index=False).encode("utf-8"),
                       file_name=f"predictions_{key}.csv", mime="text/csv", key=f"dl_{key}")


# ---------------------------------------------------------------------------
# Le modèle
# ---------------------------------------------------------------------------
def about_tab(key, cfg, reg):
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        st.html(f"""<div class="h2">Comparaison des algorithmes</div>
<p class="small" style="margin-top:.8rem;font-size:.95rem">{esc(cfg['metric_name'])} obtenu par chaque algorithme
sur les données de validation (10 % du dataset), après recherche des meilleurs paramètres par validation croisée.
Le modèle déployé est mis en évidence.</p>""" +
                ui.bars(cfg["comparison"], cfg["algo"], lambda v: fmt_num(v, 3)))
        if key == "car_data":
            ui.note("L'arbre de décision devance le Random Forest de 0,4 point, soit environ 2 voitures sur 551 : "
                    "les deux modèles sont pratiquement à égalité.")
        extra = "".join(f'<div class="stat"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>'
                        for k, v in cfg["extra_metrics"])
        if extra:
            st.html(f'<div class="stats" style="grid-template-columns:repeat({len(cfg["extra_metrics"])},minmax(0,1fr));'
                    f'margin-top:1.6rem">{extra}</div>')
    with right:
        steps = [
            ("Encodage", "Variables catégorielles transformées en nombres (LabelEncoder)."),
            ("Valeurs aberrantes", "Détectées par la méthode IQR puis remplacées par KNNImputer."),
            ("Normalisation", f"Variables mises à l'échelle avec {METHOD[key]}."),
            ("Découpage", "80 % entraînement, 10 % validation, 10 % test."),
            ("Optimisation", "GridSearchCV avec validation croisée à 5 plis."),
        ]
        st.html('<div class="h2">Méthode</div><div style="margin-top:1.2rem">' + "".join(
            f'<div style="display:grid;grid-template-columns:2.4rem 1fr;gap:.6rem;padding:.85rem 0;'
            f'border-top:1px solid var(--border)"><span class="mono" style="color:var(--faint);font-size:.8rem">'
            f'{i + 1:02d}</span><div><div style="color:var(--ink);font-weight:600;font-size:.95rem">{esc(t)}</div>'
            f'<div class="small" style="margin-top:.15rem">{esc(d)}</div></div></div>'
            for i, (t, d) in enumerate(steps)) + '</div>')
    st.html('<div class="rule"></div><div class="h2">Variables utilisées</div><div style="height:1rem"></div>')
    rows = pd.DataFrame([{"Variable": f["name"], "Libellé": f["label"],
                          "Type": "Catégorielle" if f["kind"] == "cat" else "Numérique"} for f in cfg["features"]])
    ui.table(rows)
