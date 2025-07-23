import streamlit as st
import pdfplumber
from PIL import Image
import altair as alt
import pandas as pd

st.set_page_config(page_title="Calculadora Financiera – Parque Industrial Sureste", layout="centered")

st.title("Calculadora Financiera – Parque Industrial Sureste")
st.markdown("Simula tus beneficios fiscales por invertir en el corredor interoceánico")

# Menú de selección
tabs = st.radio("Selecciona una opción:", ["Subir declaración anual (PDF)", "Llenar datos manualmente"])

if tabs == "Subir declaración anual (PDF)":
    pdf_file = st.file_uploader("Sube tu declaración anual en PDF", type="pdf")
    texto = ""
    if pdf_file is not None:
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        texto += content
        except:
            st.warning("No se pudo leer el PDF. Asegúrate de subir un archivo con texto o usa la opción manual.")

        ingresos = 0
        coef = 0

        if "187,500,000" in texto:
            ingresos = 187500000
        if "Coeficiente de utilidad 0.30" in texto:
            coef = 0.30
        elif "Coeficiente de utilidad 0.20" in texto:
            coef = 0.20

        inversion = 20000000

        if ingresos and coef:
            isr = ingresos * coef * 0.30
            iva = inversion * 0.45
            total = isr + iva
            st.success("Resultados estimados:")
            st.write(f"Crédito Fiscal ISR: ${isr:,.2f} USD")
            st.write(f"Crédito Fiscal IVA: ${iva:,.2f} USD")
            st.write(f"**Total ahorro anual estimado: ${total:,.2f} USD**")
        else:
            st.warning("No se encontraron datos claros en el PDF. Intenta llenar manualmente.")

elif tabs == "Llenar datos manualmente":
    st.subheader("Ingresa los datos para simular tus ahorros fiscales")
    ingresos = st.number_input("Ingresos acumulables (USD)", min_value=0, step=1000000)
    coef = st.selectbox("Coeficiente de utilidad", [0.20, 0.25, 0.30])
    inversion = st.number_input("Inversión en activo fijo (USD)", min_value=0, step=500000)

    st.markdown("---")
    st.subheader("Información del terreno")
    hectareas = st.number_input("Cantidad de hectáreas del proyecto", min_value=0.0, step=0.5)
    precio_m2 = st.number_input("Precio del metro cuadrado (USD)", value=70.0, step=1.0)
    valor_tierra = hectareas * 10000 * precio_m2

    st.write(f"Valor estimado de la tierra: ${valor_tierra:,.2f} USD")

    predial_percent = st.slider("% estimado de impuesto predial anual", min_value=4.5, max_value=5.0, value=4.5, step=0.1)
    ahorro_predial_anual = valor_tierra * (predial_percent / 100)
    st.write(f"Ahorro estimado anual por predial: ${ahorro_predial_anual:,.2f} USD")

    st.markdown("---")
    st.subheader("Estímulos estatales adicionales")
    estimulos = {
        "Uso de suelo (licencia)": st.checkbox("✓ Uso de suelo (licencia)"),
        "Protección civil": st.checkbox("✓ Protección civil"),
        "Vehículos usados": st.checkbox("✓ Vehículos usados"),
        "Registro de propiedad": st.checkbox("✓ Registro de propiedad"),
        "Dictamen ambiental": st.checkbox("✓ Dictamen ambiental")
    }

    ahorro_estatal = 0
    for nombre, activo in estimulos.items():
        if activo:
            monto = st.number_input(f"Monto estimado por '{nombre}' (USD)", min_value=0, step=5000, key=nombre)
            ahorro_estatal += monto

    if st.button("Calcular"):
        isr = ingresos * coef * 0.30
        iva = inversion * 0.45
        ahorro_anual = isr + iva + ahorro_predial_anual
        ahorro_sexenal = ahorro_anual * 6
        ahorro_8anios = ahorro_anual * 8

        total_estatal_sexenal = ahorro_estatal * 6
        total_estatal_8anios = ahorro_estatal * 8

        ahorro_total_sexenal = ahorro_sexenal + total_estatal_sexenal
        ahorro_total_8anios = ahorro_8anios + total_estatal_8anios

        st.success("Resultados estimados:")
        st.write(f"Crédito Fiscal ISR: ${isr:,.2f} USD")
        st.write(f"Crédito Fiscal IVA: ${iva:,.2f} USD")
        st.write(f"Ahorro por predial: ${ahorro_predial_anual:,.2f} USD")
        st.write(f"Ahorro estatal anual: ${ahorro_estatal:,.2f} USD")

        st.markdown("---")
        st.subheader("Proyección de ahorro")
        st.write(f"**Ahorro total anual estimado:** ${ahorro_anual + ahorro_estatal:,.2f} USD")
        st.write(f"**Proyección sexenal (6 años):** ${ahorro_total_sexenal:,.2f} USD")
        st.write(f"**Proyección a 8 años:** ${ahorro_total_8anios:,.2f} USD")

        df = pd.DataFrame({
            'Periodo': ['Anual', 'Sexenal', '8 años'],
            'Ahorro estimado (USD)': [ahorro_anual + ahorro_estatal, ahorro_total_sexenal, ahorro_total_8anios]
        })

        chart = alt.Chart(df).mark_bar().encode(
            x='Periodo',
            y='Ahorro estimado (USD)',
            tooltip=['Periodo', 'Ahorro estimado (USD)']
        ).properties(title='Proyección de ahorro total')

        st.altair_chart(chart, use_container_width=True)
