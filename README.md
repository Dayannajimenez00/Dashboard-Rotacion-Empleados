# Dashboard de rotación de empleados — IBM HR Analytics

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un dashboard interactivo para analizar la rotación de empleados utilizando el conjunto de datos IBM HR Analytics Employee Attrition & Performance, compuesto por 1.470 registros y 35 variables. La información contiene características personales, laborales y salariales de los empleados.

El propósito del análisis es identificar patrones relacionados con la permanencia y el retiro del personal, explorando variables como la edad, el departamento, el nivel del cargo y los ingresos mensuales. Se busca facilitar la comprensión de los datos y aportar información que pueda orientar decisiones relacionadas con la gestión del talento humano.

La aplicación fue desarrollada en Python utilizando Streamlit, Pandas, Plotly y SciPy. Incluye filtros interactivos, indicadores, visualizaciones, una comparación estadística de ingresos y una narrativa analítica dirigida a personas sin conocimientos técnicos.

## Dashboard publicado

Consulta la aplicación interactiva en Streamlit Community Cloud:

https://dashboard-rotacion-empleados-rgk9fwtahenszx5ulcrfxb.streamlit.app/

Captura de pantalla del dashboard

La siguiente imagen corresponde a la aplicación en funcionamiento:

<img width="1910" height="1030" alt="Screenshot 2026-11-25 225941" src="https://github.com/user-attachments/assets/baa32104-821c-475c-9809-b065b5666718" />

## Hallazgos principales del análisis

- De los 1.470 empleados analizados, 237 registraron retiro de la organización, equivalentes aproximadamente al 16,12 %.

- El ingreso mensual promedio de los empleados que permanecieron fue de $6.832,74.

- El ingreso mensual promedio de los empleados que se retiraron fue de $4.787,09.

- Se observan diferencias en los ingresos mensuales según el nivel del cargo y el departamento.

- La prueba t de Welch encontró una diferencia estadísticamente significativa entre los ingresos promedio de quienes permanecieron y quienes se retiraron.

Estos resultados muestran diferencias entre grupos, pero no demuestran que el salario sea la causa directa de la rotación.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- SciPy
- GitHub
- Streamlit Community Cloud

## Estructura del repositorio

Dashboard-Rotacion-Empleados/
│
├── app.py
├── WA_Fn-UseC_-HR-Employee-Attrition.csv
├── requirements.txt
├── README.md
└── capturas/
    └── dashboard.png

## Instalación y ejecución local

Para ejecutar el proyecto en un equipo local, sigue estos pasos:

1. Clonar el repositorio
git clone https://github.com/Dayannajimenez00/Dashboard-Rotacion-Empleados.git

2. Ingresar a la carpeta del proyecto
cd Dashboard-Rotacion-Empleados

3. Instalar las dependencias
pip install -r requirements.txt

4. Ejecutar la aplicación
streamlit run app.py

5. Abrir el dashboard
Abre en el navegador la dirección local que proporciona Streamlit, normalmente:

http://localhost:8501

## Información académica

Estudiante: Jhelenm Dayanna Jiménez Narváez
Curso: Programación para el análisis de datos
Universidad: Universidad Nacional Abierta y a Distancia (UNAD)
Grupo: G26
Actividad: Tarea 4
Fecha: 06 de diciembre de 2026

Fuente de los datos
IBM HR Analytics Employee Attrition & Performance.

Proyecto académico desarrollado con fines educativos para aplicar herramientas de programación y análisis de datos en el estudio de la rotación de empleados.


