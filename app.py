import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from scipy.stats import ttest_ind

st.set_page_config(
    page_title="Análisis de rotación de empleados",
    page_icon="📊",
    layout="wide")

st.title("Dashboard de rotación de empleados")
st.subheader("IBM HR Analytics Employee Attrition & Performance")

st.markdown("""
Este dashboard permite explorar la rotación de empleados,
sus características laborales y la distribución de sus ingresos.
Utilice los filtros laterales para examinar diferentes grupos.""")

ruta_csv = Path(__file__).parent / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

@st.cache_data
def cargar_datos(ruta):
    return pd.read_csv(ruta)

try:
    df = cargar_datos(ruta_csv)
except Exception as e:
    st.error(f"Error al cargar el dataset: {e}")
    st.stop()

st.sidebar.header("Filtros de exploración")

departamentos = sorted(df["Department"].dropna().unique())

seleccion_departamento = st.sidebar.multiselect(
    "Departamento",
    options=departamentos,
    default=departamentos)

edad_min = int(df["Age"].min())
edad_max = int(df["Age"].max())

rango_edad = st.sidebar.slider(
    "Rango de edad",
    min_value=edad_min,
    max_value=edad_max,
    value=(edad_min, edad_max))

ingreso_min = int(df["MonthlyIncome"].min())
ingreso_max = int(df["MonthlyIncome"].max())

rango_ingreso = st.sidebar.slider(
    "Rango de ingreso mensual",
    min_value=ingreso_min,
    max_value=ingreso_max,
    value=(ingreso_min, ingreso_max))

datos = df[
    (df["Department"].isin(seleccion_departamento)) &
    (df["Age"].between(*rango_edad)) &
    (df["MonthlyIncome"].between(*rango_ingreso))].copy()

if datos.empty:
    st.warning("No hay registros con los filtros seleccionados.")
    st.stop()

st.header("Indicadores principales")

total = len(datos)
retiros = (datos["Attrition"] == "Yes").sum()
tasa = retiros / total * 100
media = datos["MonthlyIncome"].mean()
desviacion = datos["MonthlyIncome"].std()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cantidad de empleados", f"{total:,}")
c2.metric("Cantidad de retiros", f"{retiros:,}")
c3.metric("Tasa de rotación", f"{tasa:.2f}%")
c4.metric("Ingreso promedio", f"${media:,.2f}")

c5, c6 = st.columns(2)
c5.metric("Media de ingresos", f"${media:,.2f}")
c6.metric("Desviación estándar", f"${desviacion:,.2f}")

st.caption(
    "Las métricas se recalculan según los filtros seleccionados.")

st.header("Visualizaciones del análisis exploratorio")

# Gráfico 1: frecuencia de rotación
st.subheader("5.1 Frecuencia de empleados según su rotación")

frecuencias = (
    datos["Attrition"]
    .value_counts()
    .rename_axis("Attrition")
    .reset_index(name="Cantidad"))

fig1 = px.bar(
    frecuencias,
    x="Attrition",
    y="Cantidad",
    color="Attrition",
    text="Cantidad",
    title="Frecuencia de empleados según su rotación",
    labels={
        "Attrition": "Rotación de empleados",
        "Cantidad": "Cantidad de empleados"})

st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: distribución de ingresos
st.subheader("5.2 Distribución de los ingresos mensuales")

fig2 = px.box(
    datos,
    y="MonthlyIncome",
    title="Distribución de los ingresos mensuales",
    labels={"MonthlyIncome": "Ingreso mensual"})

st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: nivel laboral e ingreso
st.subheader("5.3 Relación entre nivel laboral e ingresos")

fig3 = px.scatter(
    datos,
    x="JobLevel",
    y="MonthlyIncome",
    color="Attrition",
    opacity=0.7,
    hover_data=["Department", "JobRole"],
    title="Relación entre nivel del cargo e ingreso mensual",
    labels={
        "JobLevel": "Nivel del cargo",
        "MonthlyIncome": "Ingreso mensual",
        "Attrition": "Rotación"})

st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: ingreso por nivel y departamento
st.subheader("5.4 Ingreso promedio por nivel laboral y departamento")

promedios = (
    datos.groupby(["JobLevel", "Department"], as_index=False)
    ["MonthlyIncome"].mean())

fig4 = px.bar(
    promedios,
    x="JobLevel",
    y="MonthlyIncome",
    color="Department",
    barmode="group",
    title="Ingreso promedio según nivel laboral y departamento",
    labels={
        "JobLevel": "Nivel del cargo",
        "MonthlyIncome": "Ingreso mensual promedio",
        "Department": "Departamento"})

st.plotly_chart(fig4, use_container_width=True)

st.header("Validación estadística")

st.markdown("""
Se aplica la prueba t de Welch para comparar el ingreso mensual
promedio de los empleados que permanecen en la organización
y aquellos que se retiran.
""")

grupo_no = datos.loc[
    datos["Attrition"] == "No", "MonthlyIncome"]

grupo_si = datos.loc[
    datos["Attrition"] == "Yes", "MonthlyIncome"]

if len(grupo_no) > 1 and len(grupo_si) > 1:

    estadistico, valor_p = ttest_ind(
        grupo_no,
        grupo_si,
        equal_var=False)

    st.write(
        f"Promedio de quienes permanecen: "
        f"${grupo_no.mean():,.2f}")

    st.write(
        f"Promedio de quienes se retiran: "
        f"${grupo_si.mean():,.2f}")

    st.write(f"Estadístico t: {estadistico:.4f}")
    st.write(f"Valor p: {valor_p:.6g}")

    if valor_p < 0.05:
        st.success(
            "Existe una diferencia estadísticamente significativa "
            "entre los ingresos promedio de los dos grupos.")
    else:
        st.info(
            "No se encontró evidencia suficiente de una diferencia "
            "estadísticamente significativa.")

else:
    st.warning(
        "No hay suficientes registros de ambos grupos "
        "para realizar la prueba estadística.")

st.caption(
    "Nivel de significancia: α = 0.05. "
    "La diferencia estadística no demuestra causalidad.")

st.header("Exploración de los datos")

st.markdown("### Resumen estadístico de variables numéricas")

st.dataframe(
    datos.select_dtypes(include="number").describe().T,
    use_container_width=True)

st.markdown("### Tabla de registros")

st.dataframe(datos, use_container_width=True)

st.download_button(
    "Descargar datos filtrados",
    data=datos.to_csv(index=False).encode("utf-8"),
    file_name="datos_filtrados.csv",
    mime="text/csv")

st.header("Validación estadística")

st.subheader("Comparación de ingresos según la rotación")

st.write("""
Se compararon los ingresos mensuales promedio de los empleados
que permanecieron en la organización y de aquellos que se retiraron.""")

st.write(
    f"**Ingreso promedio de quienes permanecieron:** "
    f"${grupo_no.mean():,.2f}")

st.write(
    f"**Ingreso promedio de quienes se retiraron:** "
    f"${grupo_si.mean():,.2f}")

st.write(f"**Estadístico t:** {estadistico:.4f}")
st.write(f"**Valor p:** {valor_p:.6g}")

if valor_p < 0.05:
    st.success("""
    **Interpretación de los resultados**

    Se encontró una diferencia entre los ingresos promedio
    de los empleados que permanecieron y los que se retiraron.
    En promedio, quienes se retiraron tenían ingresos mensuales
    inferiores a los de quienes permanecieron.

    Esto indica que existe una relación entre los ingresos
    mensuales y la rotación de empleados en los datos analizados.
    Sin embargo, no significa que el salario sea la causa directa
    de los retiros.""")
else:
    st.info("""
    **Interpretación de los resultados**

    No se encontró evidencia suficiente para afirmar que
    los ingresos promedio de ambos grupos sean diferentes.""")

st.header("Hallazgos e interpretación")

st.subheader("¿Qué analicé?")
st.markdown("""
Se analizó el conjunto de datos **IBM HR Analytics Employee Attrition & Performance**,
que contiene información de 1.470 empleados y 35 variables relacionadas con
sus características personales y laborales. Entre los aspectos estudiados se
encuentran la edad, el departamento, el nivel del cargo, los ingresos mensuales
y la permanencia o retiro de los empleados de la organización.
""")

st.subheader("¿Qué encontré?")
st.markdown("""
En el conjunto completo de datos, 237 empleados se retiraron, lo que representa
aproximadamente el 16,12 % del personal analizado. También se encontró que el
ingreso mensual promedio de quienes permanecieron fue de **$6.832,74**,
mientras que el de quienes se retiraron fue de **$4.787,09**.

Además, las visualizaciones permiten observar diferencias en los ingresos
según el nivel del cargo y comparar la cantidad de empleados que permanecen
y que se retiran.""")

st.subheader("¿Qué significa?")
st.markdown("""
Estos resultados muestran que existen diferencias entre los grupos de empleados.
En particular, quienes se retiraron registraron un ingreso mensual promedio
inferior al de quienes permanecieron. Esta diferencia permite identificar
una posible relación entre la remuneración y la rotación, pero no demuestra
que el salario sea la causa directa de los retiros.

Por esta razón, también es importante considerar otros aspectos, como las
oportunidades de crecimiento, el departamento y las condiciones laborales.""")

st.subheader("¿Qué se recomendaría?")
st.markdown("""
Se recomienda revisar las condiciones salariales y las oportunidades de
desarrollo profesional, especialmente en los grupos donde se observe una
mayor frecuencia de retiros. También conviene realizar un seguimiento de
la rotación por departamento y nivel del cargo, con el propósito de identificar
áreas que requieran mayor atención.

Estas acciones pueden ayudar a orientar decisiones de gestión del talento
humano y promover estrategias para mejorar la permanencia de los empleados.""")

st.subheader("Visualizaciones que respaldan los hallazgos")

st.plotly_chart(fig1, use_container_width=True, key="grafica_hallazgos_1")
st.plotly_chart(fig2, use_container_width=True, key="grafica_hallazgos_2")

st.caption("Fuente: IBM HR Analytics Employee Attrition & Performance.")
