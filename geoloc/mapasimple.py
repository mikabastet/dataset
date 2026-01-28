
import pandas as pd
import matplotlib.pyplot as plt


df_textual = pd.read_excel(
    r"C:\Users\mika\Downloads\dataset_geo_simple.xlsx"
)

df_geo = pd.read_excel(
    r"C:\Users\mika\Downloads\dataset_geo_test.xlsx"
)


df_merge = df_textual.merge(
    df_geo[["Link Original", "lat", "lon"]],
    on="Link Original",
    how="left"
)

def asignar_zona_geo(lat, lon):
    if pd.isna(lat):
        return None
    if lat > -27.47:
        return "Norte"
    elif lat < -27.50:
        return "Sur"
    elif lon > -58.82:
        return "Este"
    else:
        return "Oeste"

df_merge["zona_geo"] = df_merge.apply(
    lambda r: asignar_zona_geo(r["lat"], r["lon"]),
    axis=1
)
df_merge["coincide_zona"] = (
    df_merge["zona"] == df_merge["zona_geo"]
)

print(df_merge["coincide_zona"].value_counts())
df_map = df_merge[df_merge["lat"].notna()].copy()

plt.figure()
plt.scatter(df_map["lon"], df_map["lat"])
plt.title("Ubicaciones geocodificadas – Corrientes")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.show()
errores = df_map[df_map["coincide_zona"] == False]