import os 
import pandas as pd
import pickle
import numpy as np

FEATURTES_LIBECO2 = ['IFNAIS', 'CRSEVS', 'DMSEVS', 'DSSEVS', 'IFVELA', 'ALAITS', 'CONFJF',
                'cifnai', 'ccrsev', 'cdmsev', 'cdssev', 'cfosse', 'cavels', 'calait',
                'IDQRSE']

FEATURTES_LIBECO3 = ['IFNAIS', 'CRSEVS', 'DMSEVS', 'DSSEVS', 'ISEVRE', 'IFVELA', 'ALAITS', 'IVMATE', 
                'COMPSS', 'CONFJF', 'FOSPSS', 'cifnai', 'ccrsev', 'cdmsev', 'cdssev', 'cfosse', 
                'cavels', 'calait']

FEATURTES_ENCHERE = [['LIBECO2_RJ', 'CAENST', 'LAC', 'HAR'], ['LIBECO2_RJ', 'CAENST', 'IDQRSE']]
MODELS_ENCHERE = ["enchere_model.pkl", "enchere_model_2.pkl"]

FEATURTES_PONAIS =   ['COFGMU', 'RAVELA', 'CONAIS_COCOFG', 'ID_MERE', 'TOUPOI']

FEATURTES_P210 =   ['CRSEVS', 'DM_sev', 'DS_sev', 'ccrsev', 'cdmsev', 'cdssev', 'RAVELA', 'ETAT', 'FOSEVS', 'ISEVRE', 'PONAIS', 'cfosse']

def pred(animal_id):
        df_taureaux = pd.read_csv("data/DATA_TAUREAUX_ANO.txt", sep=";", low_memory=False)

        # Vérifier si l'ID existe dans le DataFrame
        animal_data = df_taureaux[df_taureaux["ID_ANIMAL"] == animal_id]

        # Récupérer toutes les colonnes de l'animal
        variables_animal = animal_data.iloc[[0]]

        result = {}

        try :
                result["p_libeco2"] = prediction(
                        variables_animal,
                        "libeco2_model.pkl",
                        FEATURTES_LIBECO2
                )
        except :
                result["p_libeco2"] = None

        try :
                result["p_libeco3"] = prediction(
                        categorie_variables(variables_animal),
                        "libeco3_model.pkl",
                        FEATURTES_LIBECO3
                )
        except :
                result["p_enchere"] = None

        variables_animal = variables_animal.copy()
        variables_animal['LIBECO2_RJ'] = result["p_libeco2"]
        for i in range(len(MODELS_ENCHERE)):
                try :
                        result["p_enchere"] =  np.expm1(prediction(
                                variables_animal,
                                MODELS_ENCHERE[i],
                                FEATURTES_ENCHERE[i]
                        ))
                        break
                except :
                        result["p_enchere"] = None

        try :
                result["p_ponais"] = prediction(
                        categorie_variables(variables_animal),
                        "ponais_model.pkl",
                        FEATURTES_PONAIS
                )
        except :
                result["p_ponais"] = None

        try :
                result["p_p210"] = prediction(
                        categorie_variables(variables_animal),
                        "p210_model.pkl",
                        FEATURTES_P210
                )
        except :
                result["p_p210"] = None

        return result

def categorie_variables(variables_animal):
        for column in variables_animal.columns:
                if variables_animal[column].dtypes == 'object':
                        # Si la colonne a des valeurs catégorielles, les convertir en catégorie
                        variables_animal[column] = variables_animal[column].astype('category')
                else:
                        # Si la colonne devrait être numérique, la convertir en numérique
                        variables_animal = variables_animal.copy()
                        variables_animal.loc[:, column] = pd.to_numeric(variables_animal[column], errors='coerce')

        return variables_animal

def load_model(model_name):
        model_path = os.path.join("models", model_name)
        try:
                with open(model_path, "rb") as f:
                        return pickle.load(f)
        except FileNotFoundError:
                print(f"Erreur : modèle {model_name} introuvable.")
                return None
        except Exception as e:
                print(f"Erreur lors du chargement du modèle {model_name} : {e}")
                return None


def prediction(variables_animal, model_name, features):
        model = load_model(model_name)
        if model is None:
                return None
        
        
        missing_features = [feature for feature in features if feature not in variables_animal.columns]
        if missing_features:
                print(f"Erreur : certaines caractéristiques sont manquantes dans les données : {missing_features}")
                return None

        return model.predict(variables_animal[features])[0]
