import streamlit as st
import base64

def display_pdf(file_bytes):
    # Codifica o PDF para ser exibido no navegador
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(page_title="Renomeador Della Volpe", layout="wide")
st.title("🚛 Renomeador de Carregamentos")

st.info("Visualize o PDF abaixo, digite os dados e baixe o arquivo renomeado.")

arquivo = st.file_uploader("Suba o arquivo PDF aqui", type=["pdf"])

if arquivo:
    # Lemos os bytes uma única vez para usar na visualização e no download
    pdf_content = arquivo.read()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Visualização")
        display_pdf(pdf_content)
        
    with col2:
        st.subheader("Dados do Arquivo")
        # Você olha para o PDF e preenche aqui rapidamente
        placa = st.text_input("Placa (ex: FDZ0H80)", "").upper().strip()
        data_input = st.text_input("Data (ex: 04.04)", "").strip()
        
        if placa and data_input:
            nome_final = f"{placa} - {data_input}.pdf"
            st.success(f"Nome gerado: **{nome_final}**")
            
            st.download_button(
                label="📥 Baixar PDF Renomeado",
                data=pdf_content,
                file_name=nome_final,
                mime="application/pdf"
            )
        else:
            st.warning("Preencha a Placa e a Data para baixar.")
