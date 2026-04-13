import streamlit as st
import fitz  # PyMuPDF
import re

def extrair_dados_simples(pdf_bytes):
    # Abre o PDF diretamente da memória
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    texto_total = ""
    
    # Extrai o texto de todas as páginas
    for pagina in doc:
        texto_total += pagina.get_text()
    
    # Se o PDF for um scan total e o get_text vier vazio, 
    # precisamos avisar o usuário, mas vamos tentar limpar o texto primeiro
    texto_limpo = texto_total.replace(" ", "").upper()
    
    # 1. Busca Placa (Ex: FDZ0H80)
    padrao_placa = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_limpo)
    placa = padrao_placa.group(0) if padrao_placa else "PLACA_NAO_ENCONTRADA"
    
    # 2. Busca Data (DD/MM/AAAA) - Tenta pegar a do "Impresso por"
    # Se não achar, pega a primeira data que aparecer
    match_data = re.search(r'(\d{2})/(\d{2})/\d{4}', texto_total)
    
    if match_data:
        data_curta = f"{match_data.group(1)}.{match_data.group(2)}"
    else:
        data_curta = "DATA_NAO_ENCONTRADA"
        
    return placa, data_curta, texto_total

# --- Interface ---
st.set_page_config(page_title="Renomeador Della Volpe", layout="wide")
st.title("🚛 Renomeador de Arquivos")

arquivo = st.file_uploader("Suba o arquivo PDF", type=["pdf"])

if arquivo:
    pdf_bytes = arquivo.read()
    placa, data, texto_bruto = extrair_dados_simples(pdf_bytes)
    
    nome_final = f"{placa} - {data}.pdf"
    
    st.divider()
    
    if placa == "PLACA_NAO_ENCONTRADA" and not texto_bruto.strip():
        st.error("⚠️ Este PDF parece ser uma imagem pura (sem camada de texto).")
        st.info("Para este tipo de arquivo, o Streamlit Cloud precisa de OCR pesado. Tente baixar o arquivo novamente do sistema original em formato PDF Digital, se possível.")
    else:
        st.success(f"✅ Nome sugerido: {nome_final}")
        
        st.download_button(
            label="📥 Baixar PDF Renomeado",
            data=pdf_bytes,
            file_name=nome_final,
            mime="application/pdf"
        )
    
    # Ajuda a debugar: mostra o que o robô está lendo
    with st.expander("Ver texto extraído pelo robô"):
        st.text(texto_bruto)
