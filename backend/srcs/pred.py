import os 
import pandas as pd
import pickle
import numpy as np
import json

FEATURTES_LIBECO2 = ['IFNAIS', 'CRSEVS', 'DMSEVS', 'DSSEVS', 'IFVELA', 'ALAITS', 'CONFJF',
                'cifnai', 'ccrsev', 'cdmsev', 'cdssev', 'cfosse', 'cavels', 'calait',
                'IDQRSE']
FEATURTES_LIBECO3 = ['IFNAIS', 'CRSEVS', 'DMSEVS', 'DSSEVS', 'ISEVRE', 'IFVELA', 'ALAITS', 'IVMATE', 
                'COMPSS', 'CONFJF', 'FOSPSS', 'cifnai', 'ccrsev', 'cdmsev', 'cdssev', 'cfosse', 
                'cavels', 'calait']
FEATURTES_ENCHERE = ['LIBECO2_RJ', 'ROB', 'HAR', 'CAENST']
FEATURTES_PNC =  ['RAVELA', 'CONAIS_COCOFG', 'ID_M_PRODUIT']
FEATURTES_P210 =  ['CRSEVS', 'DMSEVS', 'DSSEVS', 'ccrsev', 'cdmsev', 'cdssev', 'RAVELA', 'ETAT']

def pred(animal_id):
        
        df_taureaux = pd.read_csv("data/DATA_TAUREAUX_ANO.txt", sep=";", low_memory=False)

        # Vérifier si l'ID existe dans le DataFrame
        animal_data = df_taureaux[df_taureaux["ID_ANIMAL"] == animal_id]

        # Récupérer toutes les colonnes de l'animal
        variables_animal = animal_data.iloc[[0]]
    
    
        result = {}
        
        result["p_libeco2"] = prediction(
            variables_animal,
            "libeco2_model.pkl",
            FEATURTES_LIBECO2
        )
        
        result["p_libeco3"] = prediction(
            categorie_variables(variables_animal),
            "libeco3_model.pkl",
            FEATURTES_LIBECO3
        )
        
        variables_animal = variables_animal.copy()
        variables_animal['LIBECO2_RJ'] = result["p_libeco2"]
        result["p_enchere"] =  np.expm1(prediction(
                variables_animal,
                "enchere_model.pkl",
                FEATURTES_ENCHERE
        ))
        
        # result["p_pnc"] = prediction(
        #     categorie_variables(variables_animal),
        #     "pnc_model.pkl",
        #     FEATURTES_PNC
        # )

        # result["p_p210"] = prediction(
        #     categorie_variables(variables_animal),
        #     "p210_model.pkl",
        #     FEATURTES_P210
        # )
        
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

def main():
        result = pred(int("019337"))
        result = {key: str(value) for key, value in result.items()}

        result = json.dumps(result)
        print(result)

main()