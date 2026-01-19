import pandas as pd
import os
import re
from difflib import get_close_matches

origen = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(origen)

limpio = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df_limpio = pd.read_excel(limpio)

inmo_stats = []
for inmo in df["inmobiliaria"].dropna().unique()[:15]:
    subset = df[df["inmobiliaria"] == inmo]
    total = len(subset)
    inmo_stats.append({
        "Inmobiliaria": inmo,
        "Total": total,
        "% Precio": subset["precio"].notna().mean() * 100,
        "% Habitaciones": subset["habitaciones"].notna().mean() * 100,
        "% Superficie": ((subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).mean()) * 100,
        "% Titulo": subset["titulo"].notna().mean() * 100,
        "% Antiguedad": subset["antiguedad"].notna().mean() * 100,
    })

df_inmo = pd.DataFrame(inmo_stats).sort_values("Total", ascending=False)
print("\nErrores por inmobiliaria (Top 15):")
print(df_inmo.round(1).to_string(index=False))

fuente_stats = []
for fuente in df["source"].dropna().unique():
    subset = df[df["source"] == fuente]
    total = len(subset)
    fuente_stats.append({
        "Fuente": fuente,
        "Total": total,
        "% Precio": subset["precio"].notna().mean() * 100,
        "% Habitaciones": subset["habitaciones"].notna().mean() * 100,
        "% Superficie": ((subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).mean()) * 100,
        "% Titulo": subset["titulo"].notna().mean() * 100,
    })

df_fuente = pd.DataFrame(fuente_stats).sort_values("Total", ascending=False)
print("\nErrores por fuente:")
print(df_fuente.round(1).to_string(index=False))

df["text_length"] = df["post_descripcion"].fillna("").str.len()
bins = [0, 100, 300, 500, 1000, float("inf")]
labels = ["Muy Corto", "Corto", "Medio", "Largo", "Muy Largo"]
df["text_cat"] = pd.cut(df["text_length"], bins=bins, labels=labels)

length_stats = []
for cat in labels:
    subset = df[df["text_cat"] == cat]
    if len(subset) == 0:
        continue
    length_stats.append({
        "Longitud": cat,
        "Registros": len(subset),
        "% Precio": subset["precio"].notna().mean() * 100,
        "% Habitaciones": subset["habitaciones"].notna().mean() * 100,
        "% Superficie": ((subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).mean()) * 100,
    })

df_length = pd.DataFrame(length_stats)
print("\nErrores según longitud de descripción:")
print(df_length.round(1).to_string(index=False))

palabras_precio = ["precio", "costo", "valor", "usd", "ars", "$", "consulta", "oferta"]
palabras_moneda = ["usd", "ars", "dólar", "peso", "uyu"]

def tiene_palabra(texto, palabras):
    if pd.isna(texto):
        return False
    texto = texto.lower()
    return any(p in texto for p in palabras)

df["tiene_precio_palabra"] = df["post_descripcion"].apply(lambda x: tiene_palabra(x, palabras_precio))
df["tiene_moneda"] = df["post_descripcion"].apply(lambda x: tiene_palabra(x, palabras_moneda))

sin_precio = df[(df["tiene_precio_palabra"]) & (df["precio"].isna())]
print(f"\nRegistros con palabra 'precio' pero sin precio extraído: {len(sin_precio)}")
print("Ejemplos:")
for texto in sin_precio["post_descripcion"].head(3):
    print(f" - {texto[:100]}...")

emoji_re = re.compile("["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\u2600-\u26FF\u2700-\u27BF]+", flags=re.UNICODE)

df["tiene_emoji"] = df["post_descripcion"].apply(lambda x: bool(emoji_re.search(str(x))) if pd.notna(x) else False)

con_emoji = df[df["tiene_emoji"]]
sin_emoji = df[~df["tiene_emoji"]]

print(f"\nRegistros con emojis: {len(con_emoji)}")
print(f"Registros sin emojis: {len(sin_emoji)}")
print(f"% Precio extraído con emojis: {con_emoji['precio'].notna().mean() * 100:.1f}%")
print(f"% Precio extraído sin emojis: {sin_emoji['precio'].notna().mean() * 100:.1f}%")

amb_no_nulo = df[df["ambientes"].notna()]["ambientes"]
print(f"\nAmbientes min: {amb_no_nulo.min()}, max: {amb_no_nulo.max()}, media: {amb_no_nulo.mean():.2f}")

amb_sospechosos = df[df["ambientes"] > 10]
print(f"Registros con ambientes > 10: {len(amb_sospechosos)}")
if len(amb_sospechosos) > 0:
    print("Ejemplos sospechosos:")
    for _, r in amb_sospechosos.head(3).iterrows():
        print(f"  Ambientes: {r['ambientes']}, Superficie: {r['superficie_cubierta']}")

ubic = df["ubicacion"].dropna()
print(f"\nTotal ubicaciones únicas: {len(ubic.unique())}")

top_20 = ubic.value_counts().head(20)
print("\nTop 20 ubicaciones:")
print(top_20)

print("\nPosibles duplicados similares:")
lista_ubic = ubic.unique().tolist()
duplicados = []
for i, u1 in enumerate(lista_ubic[:100]):
    similares = get_close_matches(u1, lista_ubic, n=3, cutoff=0.85)
    if len(similares) > 1:
        duplicados.append(similares)

for grupo in duplicados[:10]:
    print(" -", grupo)

fallos = []

for fuente in df["source"].dropna().unique():
    sub = df[df["source"] == fuente]
    fallos.append({
        "Escenario": f"Fuente: {fuente}",
        "Registros": len(sub),
        "% Fallo Precio": (1 - sub["precio"].notna().mean()) * 100,
        "% Fallo Superficie": (1 - (sub["superficie_cubierta"].notna() | sub["superficie_total"].notna()).mean()) * 100,
    })

for cat in ["Muy Corto", "Corto", "Medio"]:
    sub = df[df["text_cat"] == cat]
    if len(sub) > 0:
        fallos.append({
            "Escenario": f"Texto: {cat}",
            "Registros": len(sub),
            "% Fallo Precio": (1 - sub["precio"].notna().mean()) * 100,
            "% Fallo Superficie": (1 - (sub["superficie_cubierta"].notna() | sub["superficie_total"].notna()).mean()) * 100,
        })

fallos.append({
    "Escenario": "Con Emojis",
    "Registros": len(con_emoji),
    "% Fallo Precio": (1 - con_emoji["precio"].notna().mean()) * 100,
    "% Fallo Superficie": (1 - (con_emoji["superficie_cubierta"].notna() | con_emoji["superficie_total"].notna()).mean()) * 100,
})
fallos.append({
    "Escenario": "Sin Emojis",
    "Registros": len(sin_emoji),
    "% Fallo Precio": (1 - sin_emoji["precio"].notna().mean()) * 100,
    "% Fallo Superficie": (1 - (sin_emoji["superficie_cubierta"].notna() | sin_emoji["superficie_total"].notna()).mean()) * 100,
})

df_fallos = pd.DataFrame(fallos).sort_values("% Fallo Precio", ascending=False)
print("\nRanking escenarios con más fallos:")
print(df_fallos.round(1).to_string(index=False))

ruta_reporte = os.path.expanduser("~/Downloads/patrones_errores.xlsx")
with pd.ExcelWriter(ruta_reporte) as writer:
    df_inmo.to_excel(writer, sheet_name="Errores por Inmobiliaria", index=False)
    df_fuente.to_excel(writer, sheet_name="Errores por Fuente", index=False)
    df_length.to_excel(writer, sheet_name="Errores por Longitud", index=False)
    df_fallos.to_excel(writer, sheet_name="Fallos Sistemáticos", index=False)

print(f"\nReporte guardado en: {ruta_reporte}")

#Analiza qué inmobiliarias tienen más datos faltantes (precio, habitaciones, superficie, título, antigüedad).
# errores según la longitud de la descripción del post.
#Busca posts que mencionan “precio” pero no tienen precio extraído.
#Detecta si hay emojis en las descripciones y compara qué tanto afecta la extracción.
#Busca barrios mal escritos con posibles duplicados similares.
#Hace ranking de fallos sistemáticos según fuente, longitud y emojis.
