import streamlit as st
import easyocr
import numpy as np
from pdf2image import convert_from_bytes
import re

# Carrega o leitor de OCR (Português e Inglês)
# O allowlist ajuda a IA a focar em letras e números, sendo mais rápido
@st.cache_resource
def load_reader():
    return easyocr.Reader(['pt', 'en'], gpu=False)

def processar_scan(pdf_bytes):
    reader = load_reader()
    # Converte apenas a primeira e a última página (onde estão os dados)
    pages = convert_from_bytes(pdf_bytes, first_page=1, last_page=4)
    
    texto_completo = ""
    for page in pages:
        # Transforma a página do PDF em um formato que a IA entende
        img_np = np.array(page)
        resultados = reader.readtext(img_np, detail=0)
        texto_completo += " ".join(resultados) + " "

    # Busca Placa (Ex: FDZ0H80)
    texto_limpo = texto_completo.replace(" ", "").upper()
    placa_match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_limpo)
    placa = placa_match.group(0) if placa_match else "PLACA_NAO_ENCONTRADA"

    # Busca Data (DD/MM/AAAA)
    data_match = re.search(r'(\d{2})/(\d{2})/\d{4}', texto_completo)
    data_curta = f"{data_match.group(1)}.{data_match.group(2)}" if data_match else "DATA_ERRO"
    
    return placa, data_curta

st.title("🚛 Leitor Automático Della Volpe")
st.info("Sistema gratuito e ilimitado. O processamento pode levar 30 segundos.")

arquivo = st.file_uploader("Suba o arquivo PDF", type=["pdf"])

if arquivo:
    pdf_content = arquivo.read()
    
    with st.spinner('A IA está analisando a imagem...'):
        try:
            placa, data = processar_scan(pdf_content)
            nome_final = f"{placa} - {data}.pdf"
            
            st.success("✅ Leitura concluída!")
            st.subheader(f"Nome sugerido: `{nome_final}`")
            
            st.download_button(
                label="📥 Baixar Arquivo Renomeado",
                data=pdf_content,
                file_name=nome_final,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
            st.warning("Se o erro persistir, o arquivo pode ser grande demais para o servidor gratuito.")
