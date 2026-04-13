import streamlit as st
import easyocr
import numpy as np
from pdf2image import convert_from_bytes
import re

# Carrega o leitor de OCR (Português)
reader = easyocr.Reader(['pt'])

def processar_arquivo(pdf_bytes):
    # Converte a primeira página do PDF para imagem
    images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
    img_array = np.array(images[0])
    
    # Lê o texto da imagem
    resultados = reader.readtext(img_array, detail=0)
    texto_total = " ".join(resultados)
    
    # 1. Busca Placa (Ex: FDZ0H80)
    # Remove espaços para garantir que o OCR não dividiu a placa
    texto_limpo = texto_total.replace(" ", "").upper()
    placa_match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_limpo)
    placa = placa_match.group(0) if placa_match else "PLACA_NAO_ENCONTRADA"
    
    # 2. Busca a data no campo "Impresso por"
    # Procuramos o padrão DD/MM/AAAA perto da palavra 'Impresso'
    data_match = re.search(r'(\d{2})/(\d{2})/\d{4}', texto_total)
    
    if data_match:
        data_curta = f"{data_match.group(1)}.{data_match.group(2)}"
    else:
        data_curta = "DATA_ERRO"
        
    return placa, data_curta

# --- Interface ---
st.title("🚛 Renomeador de Scans Della Volpe")

arquivo = st.file_uploader("Suba o scan em PDF aqui", type=["pdf"])

if arquivo:
    with st.spinner('Lendo imagem... (Isso leva uns 10 segundos na primeira vez)'):
        pdf_content = arquivo.read()
        placa, data = processar_arquivo(pdf_content)
        
        nome_final = f"{placa} - {data}.pdf"
        
        st.success("Leitura Finalizada!")
        st.subheader(f"Sugestão de nome: `{nome_final}`")
        
        st.download_button(
            label="📥 Baixar Arquivo com Novo Nome",
            data=pdf_content,
            file_name=nome_final,
            mime="application/pdf"
        )
