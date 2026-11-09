import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard de Notas - USS",
    page_icon="📊",
    layout="wide"
)

# Carga de datos optimizada
@st.cache_data
def load_data():
    return pd.read_csv("estudiantes_notas.csv")

df = load_data()

# --- BARRA LATERAL ---
st.sidebar.image("logo u.jpg", width=200)
st.sidebar.title("Panel de Control")
st.sidebar.markdown("---")

st.sidebar.subheader("Filtros de Búsqueda")
secciones_disponibles = ["Todas"] + list(df["seccion"].unique())
seccion_seleccionada = st.sidebar.selectbox("Seleccionar Sección:", secciones_disponibles)

# Filtrar dataset según la sección elegida
if seccion_seleccionada != "Todas":
    df_filtered = df[df["seccion"] == seccion_seleccionada]
else:
    df_filtered = df

st.sidebar.markdown("---")
st.sidebar.info("💡 **Estado:** Datos cargados correctamente desde `estudiantes_notas.csv`.")


# --- ÁREA PRINCIPAL ---
st.title("📊 Dashboard de Rendimiento Académico - USS")
st.markdown("Plataforma interactiva para el seguimiento de calificaciones, asistencia y métricas grupales de los estudiantes.")

# Tarjetas de Métricas Principales (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Estudiantes", len(df_filtered))
col2.metric("Promedio Nota 1", round(df_filtered["nota_1"].mean(), 2))
col3.metric("Promedio Nota 2", round(df_filtered["nota_2"].mean(), 2))
col4.metric("Asistencia Media", f"{round(df_filtered['asistencia'].mean(), 1)}%")

st.markdown("---")

# Tabla interactiva
st.subheader("📋 Registro Detallado de Estudiantes")
st.dataframe(df_filtered, use_container_width=True)

st.markdown("---")

# Visualización Gráfica
st.subheader("📈 Análisis Gráfico de Desempeño")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("**Comparativa de Notas por Estudiante**")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df_filtered["estudiante"], df_filtered["nota_1"], color="#1f77b4", label="Nota 1")
    ax.bar(df_filtered["estudiante"], df_filtered["nota_2"], bottom=df_filtered["nota_1"], color="#ff7f0e", label="Nota 2", alpha=0.8)
    ax.set_xlabel("Estudiante")
    ax.set_ylabel("Calificación")
    plt.xticks(rotation=45, ha="right")
    ax.legend()
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    st.pyplot(fig)

with col_g2:
    st.markdown("**Relación Edad vs Asistencia (%)**")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(df_filtered["edad"], df_filtered["asistencia"], color="#2ca02c", s=100, zorder=3)
    ax.set_xlabel("Edad")
    ax.set_ylabel("Asistencia (%)")
    ax.grid(True, linestyle=":", alpha=0.6)
    st.pyplot(fig)
