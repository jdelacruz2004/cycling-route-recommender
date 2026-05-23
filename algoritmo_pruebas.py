import pandas as pd
import numpy as np
from algoritmo_2_recomendacion import recommend_routes

# Cargamos y preparamos el dataset
df = pd.read_csv('dataset/strava_data.csv')

df = df[df['sport_type'] == 'Ride']
df = df[["name", "distance", "moving_time", "total_elevation_gain", "average_speed", "sport_type", "date"]]

df = df.drop_duplicates()
df = df[df["average_speed"] > 5]
df = df[df["average_speed"] < 60]

# Clasificación de nivel
speed_conditions = [
    df["average_speed"] < 20,
    (df["average_speed"] >= 20) & (df["average_speed"] < 30),
    df["average_speed"] >= 30
]

speed_ranges = ["< 20 km/h", "20–30 km/h", "> 30 km/h"]
levels = ["Beginner", "Intermediate", "Advanced"]

import numpy as np
df = df.assign(
    speed_range=np.select(speed_conditions, speed_ranges, default="unknown"),
    level=np.select(speed_conditions, levels, default="unknown")
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

# Normalización y scoring
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

# Pruebas
print("\n=== Rutas para Beginner ===")
print(recommend_routes("Beginner", df))

print("\n=== Rutas para Intermediate ===")
print(recommend_routes("Intermediate", df))

print("\n=== Rutas para Advanced ===")
print(recommend_routes("Advanced", df))