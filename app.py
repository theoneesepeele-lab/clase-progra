import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página en modo ancho (wide)
st.set_page_config(
    page_title="Dashboard interactivo de notas",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 1. BARRA LATERAL (Datos y filtros)
# ==========================================
st.sidebar.image("logo u.jpg", width=200)
st.sidebar.title("Datos y filtros")
st.sidebar.subheader("Carga el archivo de estudiantes")

# Componente obligatorio para subir el CSV desde la página web
uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

# ==========================================
# 2. ÁREA PRINCIPAL
# ==========================================
st.title("Dashboard interactivo de notas")
st.markdown("Explora los resultados de un curso combinando filtros. **Promedio**: 50 % de cada evaluación. **Aprobación del ejercicio**: promedio mayor o igual a 4,0. Datos ficticios.")

# Validar si el usuario ya subió el archivo
if uploaded_file is not None:
    # Leer el archivo subido por el usuario
    df = pd.read_csv(uploaded_file)
    
    # Calcular el promedio de cada estudiante
    df["Promedio"] = (df["nota_1"] + df["nota_2"]) / 2

    st.sidebar.markdown("---")

    # Filtro de Sexo (Multiselect interactivo)
    st.sidebar.markdown("**Sexo**")
    sexos_disponibles = list(df["sexo"].unique())
    sexos_seleccionados = st.sidebar.multiselect(
        "Sexo", 
        options=sexos_disponibles, 
        default=sexos_disponibles,
        label_visibility="collapsed"
    )

    # Filtro de Sección
    st.sidebar.markdown("**Sección**")
    secciones_disponibles = ["Todas"] + list(df["seccion"].unique())
    seccion_seleccionada = st.sidebar.selectbox(
        "Sección", 
        options=secciones_disponibles,
        label_visibility="collapsed"
    )

    # Filtro de Rango del promedio (Slider)
    st.sidebar.markdown("**Rango del promedio**")
    rango_promedio = st.sidebar.slider(
        "Rango del promedio",
        min_value=1.0,
        max_value=7.0,
        value=(1.0, 7.0),
        step=0.1,
        label_visibility="collapsed"
    )

    # Filtro de Asistencia mínima
    st.sidebar.markdown("**Asistencia mínima (%)**")
    asistencia_minima = st.sidebar.number_input(
        "Asistencia mínima (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        label_visibility="collapsed"
    )

    st.sidebar.caption("Los filtros se combinan. Quitar ambos sexos deja la selección vacía.")

    # Aplicar los filtros a los datos
    df_filtered = df.copy()
    if sexos_seleccionados:
        df_filtered = df_filtered[df_filtered["sexo"].isin(sexos_seleccionados)]
    else:
        df_filtered = df_filtered.iloc[0:0]

    if seccion_seleccionada != "Todas":
        df_filtered = df_filtered[df_filtered["seccion"] == seccion_seleccionada]

    df_filtered = df_filtered[
        (df_filtered["Promedio"] >= rango_promedio[0]) & 
        (df_filtered["Promedio"] <= rango_promedio[1]) & 
        (df_filtered["asistencia"] >= asistencia_minima)
    ]

    # Texto de filtros activos dinámico
    sexos_str = ", ".join(sexos_seleccionados) if sexos_seleccionados else "Ninguno"
    st.markdown(f"**Filtros activos**: Sexo: {sexos_str} · Sección: {seccion_seleccionada} · Promedio: {rango_promedio[0]:.1f} a {rango_promedio[1]:.1f} · Asistencia mínima: {asistencia_minima} %")

    st.markdown("---")

    # Fila de Métricas Principales (KPIs)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown("Estudiantes seleccionados")
        st.subheader(str(len(df_filtered)))

    with col2:
        promedio_general_val = round(df_filtered["Promedio"].mean(), 2) if len(df_filtered) > 0 else 0.0
        st.markdown("Promedio general")
        st.subheader(f"{promedio_general_val:.2f}".replace(".", ","))

    with col3:
        if len(df_filtered) > 0:
            aprobados = len(df_filtered[df_filtered["Promedio"] >= 4.0])
            porcentaje_aprobacion = (aprobados / len(df_filtered)) * 100
        else:
            porcentaje_aprobacion = 0.0
        st.markdown("Aprobación")
        st.subheader(f"{porcentaje_aprobacion:.2f}%".replace(".", ","))

    st.markdown("---")

    # Controles de Visualización y Checkbox para Mostrar Tabla
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        st.markdown("Gráfico")
        tipo_grafico = st.radio(
            "Gráfico",
            options=["Notas por estudiante", "Promedio por sección"],
            horizontal=True,
            label_visibility="collapsed"
        )

    with col_ctrl2:
        mostrar_tabla = st.checkbox("Mostrar tabla", value=True)

    st.markdown("### Visualización de notas")

    col_izq, col_der = st.columns(2) if mostrar_tabla else (st.container(), None)

    with col_izq:
        if len(df_filtered) > 0:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            
            if tipo_grafico == "Notas por estudiante":
                ax.bar(df_filtered["estudiante"], df_filtered["Promedio"], color="#1f77b4")
                ax.axhline(y=4.0, color="red", linestyle="--", label="Aprobación: 4,0")
                ax.set_ylabel("Promedio de notas")
                ax.set_xlabel("Estudiante")
                plt.xticks(rotation=45, ha="right")
                ax.legend(loc="upper right", frameon=False)
            else:
                df_seccion = df_filtered.groupby("seccion")["Promedio"].mean().reset_index()
                ax.bar(df_seccion["seccion"], df_seccion["Promedio"], color="#2ca02c")
                ax.axhline(y=4.0, color="red", linestyle="--", label="Aprobación: 4,0")
                ax.set_ylabel("Promedio General")
                ax.set_xlabel("Sección")
                ax.legend(loc="upper right", frameon=False)
                
            ax.set_ylim(0, 7)
            ax.grid(axis='y', linestyle=':', alpha=0.6)
            st.pyplot(fig)
        else:
            st.warning("No hay datos disponibles con los filtros seleccionados.")

    if mostrar_tabla and col_der is not None:
        with col_der:
            st.markdown("### Estudiantes seleccionados")
            df_display = df_filtered[["id", "estudiante", "sexo", "seccion", "Promedio", "asistencia"]].copy()
            df_display["Promedio"] = df_display["Promedio"].round(2)
            df_display = df_display.rename(columns={"asistencia": "Asistencia (%)"})
            st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("---")

    if len(df_filtered) > 0:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar selección CSV",
            data=csv_data,
            file_name="estudiantes_filtrados.csv",
            mime="text/csv"
        )

    st.caption(f"Mostrando {len(df_filtered)} de {len(df)} estudiantes. La asistencia solo se usa como filtro; la aprobación depende del promedio.")

else:
    # Mensaje inicial cuando aún no se ha subido ningún archivo
    st.info("👈 **Por favor, sube el archivo `estudiantes_notas.csv` en la barra lateral izquierda** para cargar y visualizar el dashboard interactivo.")
