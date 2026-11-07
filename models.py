"""Configuration des quatre modèles et fonctions de prédiction."""
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Traductions affichées dans les listes déroulantes (la valeur envoyée au
# modèle reste la valeur d'origine du dataset)
# ---------------------------------------------------------------------------
FR = {
    "Morning": "Matin", "Afternoon": "Après-midi", "Evening": "Soirée", "Night": "Nuit",
    "Weekday": "Semaine", "Weekend": "Week-end",
    "Low": "Faible", "Medium": "Moyen", "High": "Dense",
    "Clear": "Dégagé", "Rain": "Pluie", "Snow": "Neige",
    "Petrol": "Essence", "Diesel": "Diesel", "CNG": "GNV",
    "Dealer": "Concessionnaire", "Individual": "Particulier",
    "Manual": "Manuelle", "Automatic": "Automatique",
}


def num(name, label, default, step, min_value=0, max_value=None, help=None):
    return dict(name=name, label=label, kind="num", default=default, step=step,
                min=min_value, max=max_value, help=help)


def cat(name, label, index, help=None):
    return dict(name=name, label=label, kind="cat", index=index, help=help)


MODELS = {
    "taxi": dict(
        number="01", kind="regression", title="Prix d'une course en taxi",
        short="Taxi", folder="taxi", model_file="rf_model.joblib", algo="Random Forest",
        lead="Estimer le prix d'un trajet à partir de la distance, de la durée, du moment "
             "de la journée, du trafic, de la météo et de la grille tarifaire.",
        rows=1000, metric_name="R²", metric=0.903,
        extra_metrics=[("RMSE", "7,17 $"), ("MAE", "5,18 $")],
        comparison=[("Régression linéaire", 0.865), ("Ridge", 0.864),
                    ("Arbre de décision", 0.792), ("Random Forest", 0.903)],
        target="Trip_Price", target_label="Prix estimé", unit="$", decimals=2,
        source="taxi_trip_pricing.csv",
        features=[
            num("Trip_Distance_km", "Distance (km)", 25.0, 0.5),
            cat("Time_of_Day", "Moment de la journée", 0),
            cat("Day_of_Week", "Type de jour", 1),
            num("Passenger_Count", "Passagers", 2, 1, min_value=1, max_value=4),
            cat("Traffic_Conditions", "Trafic", 2),
            cat("Weather", "Météo", 3),
            num("Base_Fare", "Prise en charge", 3.5, 0.1),
            num("Per_Km_Rate", "Tarif au km", 1.2, 0.05),
            num("Per_Minute_Rate", "Tarif à la minute", 0.3, 0.01),
            num("Trip_Duration_Minutes", "Durée (minutes)", 60.0, 1.0),
        ],
    ),
    "telephone": dict(
        number="02", kind="classification", title="État d'un téléphone",
        short="Téléphone", folder="telephone", model_file="rf_model.joblib", algo="Random Forest",
        lead="Déterminer si un téléphone mis en vente à Dakar est neuf, d'occasion, "
             "reconditionné ou venant, à partir de son prix et de ses caractéristiques.",
        rows=3253, metric_name="Accuracy", metric=0.874,
        extra_metrics=[("Classes", "4")],
        comparison=[("Régression logistique", 0.683), ("Arbre de décision", 0.812),
                    ("Random Forest", 0.874)],
        target="etat", target_label="État prédit", source="Telephone_data.csv",
        features=[
            num("prix", "Prix (FCFA)", 250000, 5000),
            cat("adresse", "Adresse", 0),
            cat("marque", "Marque", 1),
            num("dim_ecr", "Écran (pouces)", 6.0, 0.1),
            num("ram", "RAM (Go)", 8, 1, min_value=1),
            num("stockage", "Stockage (Go)", 128, 1, min_value=1),
        ],
    ),
    "car_data": dict(
        number="03", kind="classification", title="Voiture venant ou d'occasion",
        short="Venant / Occasion", folder="car_data", model_file="dt_model.joblib",
        algo="Arbre de décision",
        lead="Prédire si une voiture vendue à Dakar arrive de l'étranger (venant) ou a déjà "
             "roulé localement (d'occasion), d'après sa marque, son année, sa boîte, son "
             "quartier et son prix.",
        rows=5507, metric_name="Accuracy", metric=0.811,
        extra_metrics=[("Classes", "2")],
        comparison=[("Régression logistique", 0.789), ("Arbre de décision", 0.811),
                    ("Random Forest", 0.808)],
        target="Venant_Occasion", target_label="Statut prédit", source="Car_Data.csv",
        features=[
            cat("Marque", "Marque", 0),
            num("Année", "Année", 2015, 1, min_value=1990, max_value=2026),
            cat("Boite_Vitesse", "Boîte de vitesses", 1),
            cat("Adresse", "Adresse", 2),
            num("Prix", "Prix (FCFA)", 7800000, 100000),
        ],
    ),
    "car_dataset": dict(
        number="04", kind="regression", title="Prix de revente d'une voiture",
        short="Prix de revente", folder="car_dataset", model_file="rf_model.joblib",
        algo="Random Forest",
        lead="Estimer le prix de revente d'une voiture à partir de son kilométrage, de son "
             "prix neuf, de son carburant, du type de vendeur, de sa boîte et de son âge.",
        rows=5861, metric_name="R²", metric=0.877,
        extra_metrics=[("RMSE", "1,29"), ("MAE", "0,97")],
        comparison=[("Régression linéaire", 0.650), ("Ridge", 0.650),
                    ("Arbre de décision", 0.844), ("Random Forest", 0.877)],
        target="Selling_Price", target_label="Prix de revente estimé", unit="", decimals=2,
        unit_note="Même unité que le prix neuf saisi.", source="Car_dataset.csv",
        features=[
            num("Kms_Driven", "Kilométrage", 70000, 1000),
            num("Present_Price", "Prix neuf", 15.0, 0.5),
            cat("Fuel_Type", "Carburant", 0),
            cat("Seller_Type", "Vendeur", 1),
            cat("Transmission", "Transmission", 2),
            num("Age", "Âge (années)", 8, 1),
        ],
    ),
}


@st.cache_resource
def load(key):
    """Charger encodeurs, modèle, valeurs uniques et scaler d'un modèle."""
    cfg = MODELS[key]
    folder = cfg["folder"]
    return dict(
        encoders=joblib.load(f"{folder}/encoders.joblib"),
        model=joblib.load(f"{folder}/{cfg['model_file']}"),
        uniques=joblib.load(f"{folder}/uniques.joblib"),
        scaler=joblib.load(f"{folder}/scaler.joblib"),
    )


def feature_names(key):
    return [f["name"] for f in MODELS[key]["features"]]


def _matrix(key, df):
    """Encoder les variables catégorielles puis normaliser, dans l'ordre d'entraînement."""
    obj = load(key)
    X = df.copy()
    for f in MODELS[key]["features"]:
        if f["kind"] == "cat":
            X[f["name"]] = obj["encoders"][f["index"]].transform(X[f["name"]].astype(str))
    return obj["scaler"].transform(X.values.astype(float))


def predict(key, df):
    """Prédire pour un DataFrame contenant les variables dans l'ordre d'entraînement.
    Retourne (prédictions, probabilités ou None, noms des classes ou None)."""
    cfg, obj = MODELS[key], load(key)
    X = _matrix(key, df)
    y = obj["model"].predict(X)
    if cfg["kind"] == "regression":
        return np.round(y.astype(float), cfg["decimals"]), None, None
    classes = list(obj["encoders"][-1].classes_)
    labels = [classes[int(v)] for v in y]
    return labels, obj["model"].predict_proba(X), classes


def prepare_csv(key, raw):
    """Aligner un CSV chargé sur les variables attendues.
    Retourne (DataFrame des variables, liste de messages d'information, erreur ou None)."""
    names = feature_names(key)
    obj = load(key)
    notes = []
    if all(n in raw.columns for n in names):
        X = raw[names].copy()
        notes.append("Colonnes reconnues par leur nom.")
    elif raw.shape[1] >= len(names):
        X = raw.iloc[:, :len(names)].copy()
        X.columns = names
        notes.append("Noms de colonnes non reconnus : les colonnes ont été lues dans l'ordre.")
    else:
        return None, notes, (f"Le fichier contient {raw.shape[1]} colonne(s), il en faut "
                             f"au moins {len(names)} : {', '.join(names)}.")
    missing = X.isnull().any(axis=1)
    if missing.any():
        rows = ", ".join(str(i + 2) for i in np.where(missing)[0][:8])
        return None, notes, (f"{int(missing.sum())} ligne(s) contiennent des valeurs manquantes "
                             f"(lignes {rows}{'…' if missing.sum() > 8 else ''} du fichier).")
    for f in MODELS[key]["features"]:
        col = X[f["name"]]
        if f["kind"] == "cat":
            known = set(obj["encoders"][f["index"]].classes_)
            unknown = sorted(set(col.astype(str)) - known)
            if unknown:
                return None, notes, (f"Valeur(s) inconnue(s) du modèle dans « {f['name']} » : "
                                     f"{', '.join(unknown[:6])}{'…' if len(unknown) > 6 else ''}.")
        else:
            if not pd.api.types.is_numeric_dtype(col):
                return None, notes, f"La colonne « {f['name']} » doit contenir des nombres."
    return X, notes, None
