import streamlit as st
from google.cloud import vision
import io
import re
import json

# Carrega as credenciais dos Secrets do Streamlit
if "gcp_service_account" in st.secrets:
    info = json.loads(st.secrets["gcp_service_account"])
    client = vision.ImageAnnotatorClient.from_service_account_info(info)
else:
    st.error("Configure as credenciais do Google Cloud nos Secrets.")

def extrair_com_google(pdf_bytes):
    # O Google Vision prefere imagens, mas para PDFs ele processa via GCS ou blocos
    # Para simplicidade e arquivos > 1MB, enviamos o conteúdo
    image = vision.Image(content=pdf_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    if texts:
        return texts[0].description
    return ""

st.title("🚛 Renomeador Profissional (Google Vision)")

arquivo = st.file_uploader("Suba o scan (PDF/Imagem)", type=["pdf", "jpg", "png"])

if arquivo:
    with st.spinner('O Google está lendo o arquivo...'):
        conteudo = arquivo.read()
        texto_extraido = extrair_com_google(conteudo)
        
        # Limpeza e busca da Placa (Baseado no seu documento FDZ0H80)
        texto_limpo = texto_extraido.replace(" ", "").upper()
        placa_match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_limpo)
        placa = placa_match.group(0) if placa_match else "PLACA_NAO_ENCONTRADA"
        
        # Busca Data no formato DD/MM/AAAA
        data_match = re.search(r'(\d{2})/(\d{2})/\d{4}', texto_extraido)
        data_curta = f"{data_match.group(1)}.{data_match.group(2)}" if data_match else "DATA_ERRO"
        
        nome_final = f"{placa} - {data_curta}.pdf"
        
        st.success(f"Pronto! Nome sugerido: {nome_final}")
        st.download_button("Baixar Arquivo Renomeado", conteudo, file_name=nome_final)
