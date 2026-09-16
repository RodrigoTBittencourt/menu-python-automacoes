import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from etl_compliance_aneel import executar_etl_completo

st.set_page_config(page_title="Painel de Controle - ANEEL", layout="centered")

st.title("🚀 Painel de Controle de Automações")
st.markdown("Gerencie e atualize os dados do Supabase diretamente pelo seu painel web.")

st.subheader("Rotina de Compliance Regulatório ANEEL")

if st.button("▶️ Executar Atualização e Enviar ao Supabase", type="primary"):
    with st.spinner("Processando dados e atualizando o Supabase... Aguarde."):
        sucesso = executar_etl_completo()
        
        if sucesso:
            st.balloons()
            
            # --- VALIDAÇÃO AUTOMÁTICA PÓS-EXECUÇÃO ---
            st.divider()
            st.subheader("📊 Status Atual no Supabase")
            
            try:
                if "DB_PASS" in st.secrets:
                    db_pass = st.secrets["DB_PASS"]
                else:
                    db_pass = "@Supabaserod988101"
                    
                string_conexao = f"postgresql+psycopg2://postgres:{db_pass}@db.tocehhtqemxhgxuwjykm.supabase.co:5432/postgres"
                engine = create_engine(string_conexao)
                
                query = "SELECT * FROM tb_compliance_regulatorio_aneel"
                df_verificacao = pd.read_sql(query, con=engine)
                
                total_linhas = len(df_verificacao)
                total_colunas = len(df_verificacao.columns)
                
                col1, col2 = st.columns(2)
                col1.metric("Total de Registros no Banco", total_linhas)
                col2.metric("Total de Colunas", total_colunas)
                
                st.markdown("**Prévia dos dados salvos no Supabase:**")
                st.dataframe(df_verificacao.head(5))
                
            except Exception as e:
                st.error(f"❌ Erro ao consultar o Supabase após o envio: {e}")