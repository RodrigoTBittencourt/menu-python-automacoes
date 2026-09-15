import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Painel de Controle de Códigos Python",
    page_icon="⚡",
    layout="centered",
)

# --- ESTILIZAÇÃO CSS (Tons de Azul e Branco) ---
st.markdown(
    """
    <style>
        /* Fundo principal da página */
        .stApp {
            background-color: #f4f8fb;
        }
        
        /* Cabeçalho / Título principal */
        h1 {
            color: #0f2d4a !important;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
        }
        
        /* Subtítulos e textos */
        p, label, span {
            color: #1a3b5c !important;
        }
        
        /* Estilização personalizada dos botões */
        .stButton>button {
            background: linear-gradient(135deg, #1b4965 0%, #3f88c5 100%);
            color: #ffffff !important;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            width: 100%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #12354c.  0%, #2c6ca1 100%);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
            border: none;
            color: #ffffff !important;
        }
        
        /* Blocos de expansão ou cartões */
        div.streamlit-expanderHeader {
            background-color: #e2ecf5;
            color: #0f2d4a;
            border-radius: 6px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CREDENCIAIS DO BANCO DE DADOS (Supabase) ---
DB_USER = "postgres"
DB_PASS = st.secrets["DB_PASS"]
DB_HOST = "db.tocehhtqemxhgxuwjykm.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


@st.cache_resource
def get_engine():
  return create_engine(DATABASE_URL)


# --- INTERFACE DO USUÁRIO ---
st.title("Painel de Controle de Códigos Python")
st.markdown(
    "<p style='text-align: center; font-size: 1.1rem;'>Central de automação"
    " de rotinas e cargas para o Supabase.</p>",
    unsafe_allow_html=True,
)

st.divider()

# --- SEÇÃO 1: RELATÓRIO ANEEL (Seu ETL atual) ---
st.markdown("### 📊 Relatório de Compliance Regulatório (ANEEL)")
st.write(
    "Executa a limpeza, tratamento de datas e valores monetários dos arquivos"
    " CSV e atualiza a tabela no Supabase."
)

if st.button("Executar ETL ANEEL", key="btn_aneel"):
  with st.spinner(
      "Processando dados da ANEEL e enviando para o Supabase..."
  ):
    try:
      # Insira aqui a chamada para a função do seu script da ANEEL
      # Exemplo:
      # engine = get_engine()
      # df_tratado = seu_processo_aneel()
      # df_tratado.to_sql('tb_compliance_regulatorio_aneel', engine, if_exists='append', index=False)

      st.success(
          "ETL da ANEEL executado com sucesso e dados salvos no Supabase!"
      )
    except Exception as e:
      st.error(f"Erro ao executar o processo: {e}")

st.divider()

# --- SEÇÃO 2: OUTRO RELATÓRIO / AUTOMAÇÃO (Exemplo Futuro) ---
st.markdown("### 📈 Relatório Secundário / Outra Automação")
st.write("Espaço reservado para o seu próximo script de automação.")

if st.button("Executar Relatório 2", key="btn_relatorio2"):
  with st.spinner("Executando rotina secundária..."):
    try:
      # Coloque a lógica do segundo código Python aqui
      st.success("Rotina secundária executada com sucesso!")
    except Exception as e:
      st.error(f"Erro ao executar: {e}")
