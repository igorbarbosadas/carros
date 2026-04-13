import streamlit as st
import pdfplumber
import re

def extrair_dados_ajustados(pdf_file):
    texto_completo = ""
    with pdfplumber.open(pdf_file) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    
    # 1. Busca Placa (Ex: FDZ0H80) [cite: 18, 157]
    padrao_placa = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_completo)
    placa = padrao_placa.group(0) if padrao_placa else "PLACA_NAO_ENCONTRADA"

    # 2. Busca Data especificamente após "Impresso por" 
    # No seu doc: "Impresso por:C017542-04/04/2026-20:38:41"
    match_impresso = re.search(r'Impresso por:.*?(\d{2})/(\d{2})/\d{4}', texto_completo)
    
    if match_impresso:
        dia = match_impresso.group(1) # Pega o DD
        mes = match_impresso.group(2) # Pega o MM
        data_curta = f"{dia}.{mes}"
    else:
        data_curta = "DATA_NAO_ENCONTRADA"
    
    return placa, data_curta

# --- Interface Streamlit ---
st.set_page_config(page_title="Renomeador de Cargas", page_icon="🚛")
st.title("🚛 Renomeador Automático")
st.write("Formato de saída: **PLACA - DD.MM.pdf**")

upload = st.file_uploader("Arraste o PDF aqui", type=["pdf"])

if upload:
    placa, data_personalizada = extrair_dados_ajustados(upload)
    
    # Monta o nome conforme solicitado: PLACA - DD.MM.pdf
    nome_final = f"{placa} - {data_personalizada}.pdf"
    
    st.divider()
    st.subheader("Resultado da Extração:")
    st.info(f"**Nome sugerido:** `{nome_final}`")
    
    # Botão para baixar com o novo nome
    st.download_button(
        label="📥 Baixar PDF Renomeado",
        data=upload,
        file_name=nome_final,
        mime="application/pdf"
    )
