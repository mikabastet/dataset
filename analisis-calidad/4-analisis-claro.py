import pandas as pd
import matplotlib.pyplot as plt
import os

path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(path)

df["tipo_operacion"] = df["tipo_operacion"].str.lower().str.strip()
df["moneda"] = df["moneda"].str.upper().str.strip()

df["precio_num"] = (
    df["precio"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.extract(r"([-+]?\d*\.?\d+)")
    .astype(float)
)

alquiler_ars = df[
    (df["tipo_operacion"].str.contains("alquiler", na=False)) &
    (df["moneda"] == "ARS") &
    (df["precio_num"] > 0)
]["precio_num"]

venta_usd = df[
    (df["tipo_operacion"].str.contains("venta", na=False)) &
    (df["moneda"] == "USD") &
    (df["precio_num"] > 0)
]["precio_num"]

def analizar_outliers(precios, etiqueta):
    Q1 = precios.quantile(0.25)
    Q3 = precios.quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers_altos = precios[precios > limite_superior]
    outliers_bajos = precios[precios < limite_inferior]

    print(f"\nAnálisis de outliers para {etiqueta}:")
    print(f"  Rango esperado: {limite_inferior:.2f} - {limite_superior:.2f}")
    print(f"  Total datos: {len(precios)}")
    print(f"  Outliers altos (> límite superior): {len(outliers_altos)}")
    print(f"  Outliers bajos (< límite inferior): {len(outliers_bajos)}")
    print(f"  Porcentaje de outliers: {(len(outliers_altos) + len(outliers_bajos))/len(precios)*100:.2f}%")

analizar_outliers(alquiler_ars, "Alquileres en ARS")
analizar_outliers(venta_usd, "Ventas en USD")


fig, ax = plt.subplots(figsize=(10,6))
ax.boxplot(
    [alquiler_ars, venta_usd],
    labels=["Alquiler (ARS)", "Venta (USD)"],
    patch_artist=True,
    boxprops=dict(facecolor="#a2d5f2", alpha=0.7),
    medianprops=dict(color="red", linewidth=2),
    showmeans=True,
    meanprops=dict(marker="D", markerfacecolor="green", markeredgecolor="green")
)
ax.set_title("Distribución de Precios por Tipo de Operación y Moneda", fontsize=14, weight='bold')
ax.set_ylabel("Precio")
ax.grid(True, axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()



