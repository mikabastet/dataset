import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(path)
total_rows = len(df)

print("\n" + "="*70)
print("ANÁLISIS INTEGRAL DE CALIDAD DEL DATASET")
print("="*70)


completitud = pd.DataFrame({
    "Campo": df.columns,
    "Registros": [df[col].notna().sum() for col in df.columns],
    "Completitud (%)": [(df[col].notna().sum() / total_rows * 100).round(1) for col in df.columns]
}).sort_values("Completitud (%)", ascending=False)

print(completitud.to_string(index=False))


duplicados = df.duplicated().sum()
duplicados_precio = df[['precio', 'tipo_operacion']].duplicated().sum()
print(f"Filas completamente duplicadas: {duplicados} ({duplicados/total_rows*100:.2f}%)")
print(f"Combinaciones precio+tipo duplicadas: {duplicados_precio}")



df['precio_num'] = pd.to_numeric(df['precio'], errors='coerce')
precios_validos = df[df['precio_num'] > 0]
precios_invalidos = df[df['precio_num'] <= 0]

print(f"Precios válidos (> 0): {len(precios_validos)} ({len(precios_validos)/total_rows*100:.1f}%)")
print(f"Precios inválidos (<= 0 o vacíos): {len(precios_invalidos)} ({len(precios_invalidos)/total_rows*100:.1f}%)")

if len(precios_validos) > 0:
    print(f"  Rango válido: ${precios_validos['precio_num'].min():,.0f} - ${precios_validos['precio_num'].max():,.0f}")
    print(f"  Precio promedio: ${precios_validos['precio_num'].mean():,.0f}")
    print(f"  Precio mediano: ${precios_validos['precio_num'].median():,.0f}")


df['tipo_operacion'] = df['tipo_operacion'].str.lower().str.strip()
tipos = df['tipo_operacion'].value_counts()

consistency = []
for tipo in tipos.index:
    subset = df[df['tipo_operacion'] == tipo]
    consistency.append({
        'Tipo': tipo.title(),
        'Total': len(subset),
        '% Precio': (subset['precio_num'].notna().sum() / len(subset) * 100).round(1),
        '% Moneda': (subset['moneda'].notna().sum() / len(subset) * 100).round(1),
        'Precio promedio': f"${subset['precio_num'].mean():,.0f}" if subset['precio_num'].notna().sum() > 0 else "N/A"
    })

consistency_df = pd.DataFrame(consistency)
print(consistency_df.to_string(index=False))


Q1 = precios_validos['precio_num'].quantile(0.25)
Q3 = precios_validos['precio_num'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

outliers = df[(df['precio_num'] < limite_inferior) | (df['precio_num'] > limite_superior)]

print(f"Outliers detectados: {len(outliers)} ({len(outliers)/total_rows*100:.2f}%)")
print(f"Rango esperado: ${limite_inferior:,.0f} - ${limite_superior:,.0f}")
print(f"Outliers por debajo de ${limite_inferior:,.0f} o por encima de ${limite_superior:,.0f}")


campos_criticos = {
    'Precio': df['precio_num'].notna().sum() / total_rows * 100,
    'Tipo operación': df['tipo_operacion'].notna().sum() / total_rows * 100,
    'Moneda': df['moneda'].notna().sum() / total_rows * 100,
    'Barrio/Ubicación': df['ubicacion'].notna().sum() / total_rows * 100,
}

for campo, pct in campos_criticos.items():
    estado = "✅" if pct >= 90 else "⚠️" if pct >= 70 else "❌"
    print(f"{estado} {campo}: {pct:.1f}% completo")


score = 0
criticos_pct = np.mean(list(campos_criticos.values()))
score += criticos_pct * 0.4

dup_score = max(0, 100 - (duplicados/total_rows*100)*2)
score += dup_score * 0.2

outlier_pct = (len(outliers)/total_rows*100)
outlier_score = max(0, 100 - outlier_pct)
score += outlier_score * 0.2

precios_score = (len(precios_validos)/total_rows*100)
score += precios_score * 0.2

score = round(score, 1)

if score >= 85:
    calidad = "EXCELENTE"
elif score >= 70:
    calidad = "BUENA"
elif score >= 50:
    calidad = "REGULAR"
else:
    calidad = "POBRE"

print(f"SCORE TOTAL: {score}/100 {calidad}\n")

print("Desglose:")
print(f"  - Completitud campos críticos: {criticos_pct:.1f}% (40%)")
print(f"  - Ausencia de duplicados: {dup_score:.1f}% (20%)")
print(f"  - Ausencia de outliers: {outlier_score:.1f}% (20%)")
print(f"  - Precios válidos: {precios_score:.1f}% (20%)")


recomendaciones = []

if criticos_pct < 90:
    recomendaciones.append("Completar mejor los campos críticos (precio, tipo, moneda, ubicación).")

if duplicados > total_rows * 0.01:
    recomendaciones.append(" Hay duplicados, revisar y eliminar registros repetidos.")

if outlier_pct > 5:
    recomendaciones.append(" Existen varios outliers, analizar precios extremos.")

if precios_score < 95:
    recomendaciones.append(" Algunos precios inválidos, limpiar datos antes de análisis.")

if not recomendaciones:
    print("Dataset en buena calidad. No se necesitan acciones urgentes.")
else:
    for rec in recomendaciones:
        print(rec)


fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análisis de Calidad del Dataset Inmobiliario', fontsize=16, fontweight='bold')

campos_criticos_dict = {k: v for k, v in campos_criticos.items()}
ax1 = axes[0, 0]
colors_comp = ['#2ecc71' if v >= 90 else '#f39c12' if v >= 70 else '#e74c3c' for v in campos_criticos_dict.values()]
ax1.barh(list(campos_criticos_dict.keys()), list(campos_criticos_dict.values()), color=colors_comp)
ax1.set_xlabel('Completitud (%)')
ax1.set_title('Campos Críticos')
ax1.axvline(90, color='green', linestyle='--', alpha=0.5, label='Excelente (90%)')
ax1.axvline(70, color='orange', linestyle='--', alpha=0.5, label='Aceptable (70%)')
ax1.legend(fontsize=8)
ax1.set_xlim(0, 105)

ax2 = axes[0, 1]
top_campos = completitud.head(10)
ax2.bar(range(len(top_campos)), top_campos['Completitud (%)'].values, color='#3498db')
ax2.set_xticks(range(len(top_campos)))
ax2.set_xticklabels(top_campos['Campo'].values, rotation=45, ha='right', fontsize=8)
ax2.set_ylabel('Completitud (%)')
ax2.set_title('Top 10 Campos Más Completos')
ax2.set_ylim(0, 105)

ax3 = axes[1, 0]
precios_valid = precios_validos['precio_num'][precios_validos['precio_num'] < precios_validos['precio_num'].quantile(0.99)]
ax3.hist(precios_valid, bins=50, color='#9b59b6', edgecolor='black', alpha=0.7)
ax3.set_xlabel('Precio')
ax3.set_ylabel('Frecuencia')
ax3.set_title(f'Distribución de Precios (n={len(precios_validos)})')
ax3.axvline(precios_valid.median(), color='red', linestyle='--', linewidth=2, label=f'Mediana: ${precios_valid.median():,.0f}')
ax3.legend()

ax4 = axes[1, 1]
score_parts = [criticos_pct * 0.4, dup_score * 0.2, outlier_score * 0.2, precios_score * 0.2]
score_labels = [
    f'Completitud\n{criticos_pct:.1f}%\n(40%)',
    f'Duplicados\n{dup_score:.1f}%\n(20%)',
    f'Outliers\n{outlier_score:.1f}%\n(20%)',
    f'Precios\n{precios_score:.1f}%\n(20%)'
]
colors_score = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
wedges, texts, autotexts = ax4.pie(score_parts, labels=score_labels, autopct='%1.0f', colors=colors_score, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax4.set_title(f'Score Total: {score}/100')

plt.tight_layout()
plt.savefig('analisis_calidad_grafico.png', dpi=150, bbox_inches='tight')
print("✅ Gráfico guardado como 'analisis_calidad_grafico.png'")
plt.show()

print("\n" + "="*70 + "\n")


plt.figure(figsize=(8,5))
plt.boxplot(precios_validos['precio_num'], vert=True, patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='blue'),
            medianprops=dict(color='red'),
            whiskerprops=dict(color='blue'),
            capprops=dict(color='blue'),
            flierprops=dict(marker='o', markerfacecolor='orange', markersize=6, linestyle='none', markeredgecolor='red'))
plt.title('Boxplot de Precios: Detectando Outliers')
plt.ylabel('Precio')
plt.grid(axis='y', alpha=0.3)
plt.show()
