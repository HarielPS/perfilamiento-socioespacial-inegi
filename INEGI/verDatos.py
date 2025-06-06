import pandas as pd
import numpy as np

archivos = {
    'Jalisco': 'jalisco.csv',
    'León': 'leon.csv',
    'Puebla': 'puebla.csv'
}

datos_inegi = {}

for estado, archivo in archivos.items():
    try:
        df = pd.read_csv(archivo, na_values='*', encoding='latin1', low_memory=False)

        # Elimina BOM en los nombres de columnas si aparece
        df.columns = df.columns.str.replace('ï»¿', '', regex=False)

        datos_inegi[estado] = df

        print(f"\n=== {estado.upper()} ===")
        print(df.isnull().sum())
    except Exception as e:
        print(f"\n[ERROR] Al cargar {archivo}: {e}")
