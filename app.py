import streamlit as st
import base64

def display_pdf(file):
    # Lê o PDF e codifica para exibição na tela
    base64_pdf = base64.b64encode(file).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_ 開き true)

st.set_page_config(page_title="Renomeador Della Volpe", layout="wide")
st.title("🚛 Renomeador de Carregamentos (Modo Assistido)")

st.info("Como o arquivo é um scan, visualize o PDF abaixo e digite a Placa e o Dia/Mês.")

arquivo = st.file_uploader("Suba o arquivo PDF aqui", type=["pdf"])

if arquivo:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Visualização do Documento")
        pdf_bytes = arquivo.read()
        display_pdf(pdf_bytes)
        
    with col2:
        st.subheader("Dados para Renomear")
        # Campos de texto para preenchimento rápido
        # Você olha para o PDF ao lado e digita
        placa = st.text_input("Placa do Veículo (ex: FDZ0H80)", "").upper().strip()
        data_input = st.text_input("Dia e Mês (ex: 04.04)", "").strip()
        
        if placa and data_input:
            nome_final = f"{placa} - {data_input}.pdf"
            st.success(f"Arquivo pronto: **{nome_final}**")
            
            # Botão de download com o nome correto
            st.download_button(
                label="📥 Baixar PDF Renomeado",
                data=pdf_bytes,
                file_name=nome_final,
                mime="application/pdf"
            )
        else:
            st.warning("Preencha a Placa e a Data para habilitar o download.")

st.divider()
st.caption("Dica: A placa costuma estar na página 1 e a data de impressão no rodapé da página 4.")
