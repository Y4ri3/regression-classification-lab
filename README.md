# Atelier de prédiction

Application Streamlit réalisée dans le cadre du devoir de Machine Learning (Licence 3). Elle regroupe quatre modèles entraînés sur quatre jeux de données :

| Page | Jeu de données | Tâche | Modèle déployé | Score |
|---|---|---|---|---|
| Taxi | taxi_trip_pricing.csv | Régression du prix d'une course | Random Forest | R² 0,903 |
| Téléphone | Telephone_data.csv | Classification de l'état d'un téléphone | Random Forest | Accuracy 0,874 |
| Venant / Occasion | Car_Data.csv | Classification binaire : venant ou d'occasion | Arbre de décision | Accuracy 0,811 |
| Prix de revente | Car_dataset.csv | Régression du prix de revente | Random Forest | R² 0,877 |

Chaque page propose une prédiction simple (formulaire) et une prédiction multiple à partir d'un fichier CSV. Un fichier d'exemple `sample_df.csv` se trouve dans le dossier de chaque modèle.

## Installation

Les modèles ont été sauvegardés avec scikit-learn 1.6.1, qui demande Python 3.12 au plus.

```
pip install -r requirements.txt
```

## Lancement

```
streamlit run Accueil.py
```

L'application s'ouvre sur http://localhost:8501.

## Organisation

`Accueil.py` est le point d'entrée. `models.py` décrit les quatre modèles et contient l'encodage, la normalisation et la prédiction. `views.py` construit les pages, `ui.py` gère le thème et le style. Les dossiers `taxi/`, `telephone/`, `car_data/` et `car_dataset/` contiennent les encodeurs, le scaler et le modèle sauvegardés avec joblib.

Auteure : Fatoumata Yarie Camara.
