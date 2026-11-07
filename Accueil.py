"""Point d'entrée de l'application : thème, navigation et pages."""
import streamlit as st

st.set_page_config(page_title="Atelier de prédiction", layout="wide", initial_sidebar_state="collapsed")

import models as M  # noqa: E402
import ui  # noqa: E402
import views  # noqa: E402

# Thème : conservé dans la session et dans l'adresse (?theme=dark) pour survivre à un rechargement
if "theme" not in st.session_state:
    st.session_state.theme = "dark" if st.query_params.get("theme") == "dark" else "light"

home = st.Page(views.home, title="Accueil", url_path="accueil", default=True)
pages = {key: st.Page(views.make_model_page(key), title=cfg["short"], url_path=key)
         for key, cfg in M.MODELS.items()}
views.PAGES.update(home=home, **pages)

nav = st.navigation([home, pages["taxi"], pages["telephone"], pages["car_data"], pages["car_dataset"]],
                    position="top")

ui.inject_css()
ui.theme_switch()
if st.session_state.theme == "dark":
    st.query_params["theme"] = "dark"
elif "theme" in st.query_params:
    del st.query_params["theme"]
nav.run()
