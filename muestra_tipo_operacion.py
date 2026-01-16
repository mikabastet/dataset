import pandas as pd
import os

file_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(file_path)

#tomar 30 datos al azar para tipo_operacion
muestra = df.sample(n=30, random_state=42)

#exportar para control manual
muestra.to_excel('muestra_tipo_operacion.xlsx', index=False)
print("Muestra de 25 avisos por tipo de operación exportada a 'muestra_tipo_operacion.xlsx'")
