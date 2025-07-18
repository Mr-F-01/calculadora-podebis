import streamlit as st
import pdfplumber

st.set_page_config(page_title="Calculadora PODEBIS", layout="centered")

st.title("Calculadora Financiera – PODEBIS | Istmo de Tehuantepec")
st.markdown("Simula tus beneficios fiscales por invertir en el corredor interoceánico")

tabs = st.radio("Selecciona una opción:", ["Subir declaración anual (PDF)", "Llenar datos manualmente"])

if tabs == "Subir declaración anual (PDF)":
    pdf_file = st.file_uploader("Sube tu declaración anual en PDF", type="pdf")
    if pdf_file is not None:
        with pdfplumber.open(pdf_file) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text()

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

    if st.button("Calcular"):
        isr = ingresos * coef * 0.30
        iva = inversion * 0.45
        total = isr + iva
        st.success("Resultados estimados:")
        st.write(f"Crédito Fiscal ISR: ${isr:,.2f} USD")
        st.write(f"Crédito Fiscal IVA: ${iva:,.2f} USD")
        st.write(f"**Total ahorro anual estimado: ${total:,.2f} USD**")
