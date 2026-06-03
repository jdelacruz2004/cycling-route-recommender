import pandas as pd
import numpy as np
import unittest
from algoritmo_recomendacion import recommend_routes

# ============================================================
# Preparación del dataset para los tests
# ============================================================
def cargar_datos():
    df = pd.read_csv('dataset/strava_data.csv')
    df = df[df['sport_type'] == 'Ride']
    df = df[["name", "distance", "moving_time", "total_elevation_gain", "average_speed", "sport_type", "date"]]
    df = df.drop_duplicates()
    df = df[df["average_speed"] > 5]
    df = df[df["average_speed"] < 60]

    speed_conditions = [
        df["average_speed"] < 20,
        (df["average_speed"] >= 20) & (df["average_speed"] < 30),
        df["average_speed"] >= 30
    ]
    df = df.assign(
        speed_range=np.select(speed_conditions, ["< 20 km/h", "20–30 km/h", "> 30 km/h"], default="unknown"),
        level=np.select(speed_conditions, ["Beginner", "Intermediate", "Advanced"], default="unknown")
    )
    df["distance"] = df["distance"] * 1.60934
    df["average_speed"] = df["average_speed"] * 1.60934
    df["total_elevation_gain"] = df["total_elevation_gain"] * 0.3048
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={
        "distance": "distance_km",
        "average_speed": "average_speed_kmh",
        "total_elevation_gain": "elevation_m"
    })
    df = df.assign(
        elev_norm=(df["elevation_m"] - df["elevation_m"].min()) / (df["elevation_m"].max() - df["elevation_m"].min()),
        dist_norm=(df["distance_km"] - df["distance_km"].min()) / (df["distance_km"].max() - df["distance_km"].min()),
        speed_norm=(df["average_speed_kmh"] - df["average_speed_kmh"].min()) / (df["average_speed_kmh"].max() - df["average_speed_kmh"].min())
    )
    df = df.assign(
        difficulty_score=(
            df["elev_norm"] * 0.5 +
            df["dist_norm"] * 0.3 +
            df["speed_norm"] * 0.2
        )
    )
    return df

# ============================================================
# Tests unitarios
# ============================================================
class TestRecommendRoutes(unittest.TestCase):

    def setUp(self):
        self.df = cargar_datos()

    # Test 1 - Beginner solo retorna rutas con score <= 0.33
    def test_beginner_score(self):
        resultado = recommend_routes("Beginner", self.df)
        self.assertIsNotNone(resultado)
        self.assertTrue(all(resultado["difficulty_score"] <= 0.33))

    # Test 2 - Intermediate solo retorna rutas entre 0.33 y 0.66
    def test_intermediate_score(self):
        resultado = recommend_routes("Intermediate", self.df)
        self.assertIsNotNone(resultado)
        self.assertTrue(all(resultado["difficulty_score"] > 0.33))
        self.assertTrue(all(resultado["difficulty_score"] <= 0.66))

    # Test 3 - Advanced solo retorna rutas con score > 0.66
    def test_advanced_score(self):
        resultado = recommend_routes("Advanced", self.df)
        self.assertIsNotNone(resultado)
        self.assertTrue(all(resultado["difficulty_score"] > 0.66))

    # Test 4 - Retorna máximo 10 rutas
    def test_max_10_rutas(self):
        resultado = recommend_routes("Beginner", self.df)
        self.assertLessEqual(len(resultado), 10)

    # Test 5 - Edge case: nivel inválido retorna None
    def test_nivel_invalido(self):
        resultado = recommend_routes("Experto", self.df)
        self.assertIsNone(resultado)

    # Test 6 - Edge case: nivel con mayúscula incorrecta
    def test_nivel_case_sensitive(self):
        resultado = recommend_routes("beginner", self.df)
        self.assertIsNone(resultado)

    # Test 7 - Edge case: nivel vacío
    def test_nivel_vacio(self):
        resultado = recommend_routes("", self.df)
        self.assertIsNone(resultado)

    # Test 8 - Edge case: DataFrame vacío
    def test_dataframe_vacio(self):
        df_vacio = self.df[self.df["difficulty_score"] < 0]
        resultado = recommend_routes("Beginner", df_vacio)
        self.assertEqual(len(resultado), 0)

    # Test 9 - Resultado tiene las columnas correctas
    def test_columnas_correctas(self):
        resultado = recommend_routes("Advanced", self.df)
        columnas_esperadas = ["name", "distance_km", "average_speed_kmh", "elevation_m", "speed_range", "difficulty_score"]
        self.assertEqual(list(resultado.columns), columnas_esperadas)

    # Test 10 - Resultados ordenados por difficulty_score
    def test_ordenado_por_score(self):
        resultado = recommend_routes("Intermediate", self.df)
        scores = list(resultado["difficulty_score"])
        self.assertEqual(scores, sorted(scores))

if __name__ == '__main__':
    unittest.main()
    
    # Test 11 - Edge case: elevacion cero no rompe el sistema
def test_elevacion_cero(self):
    df_plano = self.df[self.df["elevation_m"] == 0]
    if len(df_plano) > 0:
        resultado = recommend_routes("Beginner", df_plano)
        self.assertIsNotNone(resultado)

# Test 12 - Edge case: velocidad en limite exacto cae en nivel correcto
def test_velocidad_limite_20(self):
    resultado = recommend_routes("Beginner", self.df)
    if resultado is not None:
        speeds = resultado["average_speed_kmh"]
        self.assertTrue(all(s <= 32.19 for s in speeds))  # 20 mph convertido

# Test 13 - Edge case: ruta corta con mucha elevacion
def test_ruta_corta_alta_elevacion(self):
    df_test = self.df[
        (self.df["distance_km"] < 15) & 
        (self.df["elevation_m"] > 500)
    ]
    if len(df_test) > 0:
        resultado = recommend_routes("Advanced", df_test)
        self.assertIsNotNone(resultado)

# Test 14 - Edge case: dataframe con un solo registro
def test_un_solo_registro(self):
    df_uno = self.df.head(1)
    resultado = recommend_routes("Beginner", df_uno)
    # No debe lanzar error, puede retornar vacío
    self.assertIsNotNone(resultado)