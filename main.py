import time
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, label_binarize, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, roc_curve, auc, 
                             confusion_matrix, ConfusionMatrixDisplay,
                             mean_absolute_error, mean_squared_error, r2_score,
                             silhouette_score, completeness_score, homogeneity_score)
import matplotlib.patches as mpatches

# --- 1. CONFIGURACIÓN INICIAL ---
print("Iniciando Pipeline de Machine Learning...")
os.makedirs('outputs', exist_ok=True)
df = pd.read_csv('sdss_sample.csv')

# ==========================================
# 2. CLASIFICACIÓN: KNN (k=5)
# ==========================================
print("\n--- Ejecutando Modelo de Clasificación (KNN) ---")
X_cls = df[['u', 'g', 'r', 'i', 'z', 'redshift']]
y_cls = df['class']
clases_unicas = y_cls.unique()
y_bin = label_binarize(y_cls, classes=clases_unicas)

X_train_c, X_test_c, y_train_c, y_test_c, _, y_test_bin = train_test_split(X_cls, y_cls, y_bin, test_size=0.30, random_state=42)

scaler_c = StandardScaler()
X_train_c_sc = scaler_c.fit_transform(X_train_c)
X_test_c_sc = scaler_c.transform(X_test_c)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_c_sc, y_train_c)
y_pred_c = knn.predict(X_test_c_sc)
y_prob_c = knn.predict_proba(X_test_c_sc)

# Guardar métricas KNN
acc = accuracy_score(y_test_c, y_pred_c)
with open('outputs/metricas_clasificacion.txt', 'w') as f:
    f.write(f"Accuracy KNN: {acc:.4f}\n")

# Gráfica KNN
fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')
cm = confusion_matrix(y_test_c, y_pred_c, labels=knn.classes_)
disp = ConfusionMatrixDisplay(cm, display_labels=knn.classes_)
disp.plot(ax=ax, cmap='Blues', colorbar=False)
ax.set_title('Matriz de Confusión - KNN', color='white')
ax.tick_params(colors='white')
plt.savefig('outputs/evaluacion_knn.png', facecolor=fig.get_facecolor())
plt.close()

# ==========================================
# 3. REGRESIÓN: Lineal 
# ==========================================
print("--- Ejecutando Modelo de Regresión Lineal ---")

X_reg = df[['u', 'g', 'r', 'i', 'z']]
y_reg = df['redshift']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.30, random_state=42)

reg = LinearRegression()
reg.fit(X_train_r, y_train_r)
y_pred_r = reg.predict(X_test_r)

# Guardar métricas Regresión
mse = mean_squared_error(y_test_r, y_pred_r)
r2 = r2_score(y_test_r, y_pred_r)
with open('outputs/metricas_regresion.txt', 'w') as f:
    f.write(f"MSE: {mse:.4f}\nR2: {r2:.4f}\n")

# Gráfica Regresión
fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')
ax.scatter(y_test_r, y_pred_r, alpha=0.7, color='#e94560')
lims = [min(y_test_r.min(), y_pred_r.min()), max(y_test_r.max(), y_pred_r.max())]
ax.plot(lims, lims, 'w--', lw=2)
ax.set_title(f'Regresión: Real vs Predicho (R2={r2:.2f})', color='white')
ax.tick_params(colors='white')
plt.savefig('outputs/evaluacion_regresion.png', facecolor=fig.get_facecolor())
plt.close()

# ==========================================
# 4. CLUSTERING: KMeans (k=3)
# ==========================================
print("--- Ejecutando Modelo de Clustering (KMeans) ---")
X_clust = df[['u', 'g', 'r', 'i', 'z']]
scaler_km = StandardScaler()
X_scaled_km = scaler_km.fit_transform(X_clust)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
y_kmeans = kmeans.fit_predict(X_scaled_km)

# Guardar métricas Clustering
sil = silhouette_score(X_scaled_km, y_kmeans)
with open('outputs/metricas_clustering.txt', 'w') as f:
    f.write(f"Silhouette Score: {sil:.4f}\n")

# Gráfica Clustering (PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled_km)

fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')
ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y_kmeans, cmap='plasma', alpha=0.7)
ax.set_title('Clusters Obtenidos (K-Means)', color='white')
ax.tick_params(colors='white')
plt.savefig('outputs/evaluacion_clustering.png', facecolor=fig.get_facecolor())
plt.close()
print("\n ¡Pipeline completado! Revisa la carpeta 'outputs/'.")   \


print("Carpeta creada. Manteniendo contenedor vivo por 60 segundos...")
time.sleep(60) 