import pandas as pd
import re

# ===============================
# 1. Cargar dataset
# ===============================

input_path = r"C:\Users\mika\Downloads\Ogappy_14_01_2026.xlsx"
output_path = r"C:\Users\mika\Downloads\dataset_con_ubicacion_alternativa.xlsx"

df = pd.read_excel(input_path)

# ===============================
# 2. Función extractor
# ===============================

def extraer_ubicacion(texto):
    if pd.isna(texto):
        return None

    texto = texto.lower()

    patrones = [
        r"barrio\s+[a-záéíóúñ\s]{3,40}",
        r"b°\s*[a-záéíóúñ\s]{3,40}",
        r"zona\s+[a-záéíóúñ\s]{3,40}",
        r"[a-záéíóúñ]+\s+\d{2,5}",   # calle + número
        r"av\.?\s*[a-záéíóúñ\s]+\d{0,5}"
    ]

    for p in patrones:
        m = re.search(p, texto)
        if m:
            return m.group(0)

    return None

# ===============================
# 3. Filtrar solo sin ubicación
# ===============================

df_sin_ubi = df[df["ubicacion"].isna()].copy()

print("Registros sin ubicación:", len(df_sin_ubi))

# ===============================
# 4. Extraer desde descripción
# ===============================

df_sin_ubi["ubicacion_alternativa"] = df_sin_ubi["post_descripcion"].apply(
    extraer_ubicacion
)

# ===============================
# 5. Guardar Excel
# ===============================

df_sin_ubi.to_excel(output_path, index=False)


print("Archivo generado:")
print(output_path)
print("Con ubicacion alternativa encontrada:")
print(df_sin_ubi["ubicacion_alternativa"].notna().sum())
