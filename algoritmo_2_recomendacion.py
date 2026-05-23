def recommend_routes(level, df):
    if level == "Beginner":
        routes = df[df["difficulty_score"] <= 0.33]
    elif level == "Intermediate":
        routes = df[(df["difficulty_score"] > 0.33) & (df["difficulty_score"] <= 0.66)]
    elif level == "Advanced":
        routes = df[df["difficulty_score"] > 0.66]
    else:
        print("Nivel no válido. Usa: Beginner, Intermediate o Advanced")
        return None

    return routes.sort_values("difficulty_score")[
        ["name", "distance_km", "average_speed_kmh", "elevation_m", "speed_range", "difficulty_score"]
    ].head(10)