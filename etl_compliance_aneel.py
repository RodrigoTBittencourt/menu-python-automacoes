import os
import glob
import pandas as pd
from sqlalchemy import create_engine, Numeric
import streamlit as st

def executar_etl_completo():
    # Detecta se está rodando no Streamlit Cloud ou no seu PC (OneDrive)
    if "DB_PASS" in st.secrets:
        PASTA_DADOS = os.getcwd()  # Na nuvem do Streamlit
        db_pass = st.secrets["DB_PASS"]
    else:
        PASTA_DADOS = r'C:\Users\r-the\OneDrive\01 - COMPLIANCE\01 - REGULATORIO'  # No seu PC (OneDrive)
        db_pass = "@Supabaserod988101"

    PADRAO_NOME = 'Compliance_Regulatorio_Aneel*.csv'
    caminho_busca = os.path.join(PASTA_DADOS, PADRAO_NOME)
    arquivos_encontrados = glob.glob(caminho_busca)

    if not arquivos_encontrados:
        st.warning(f"Nenhum arquivo encontrado com o padrão '{PADRAO_NOME}' em: {PASTA_DADOS}")
        return False
    
    st.info(f"Foram encontrados {len(arquivos_encontrados)} arquivo(s). Iniciando pipeline...")
    
    lista_dfs = []
    colunas_referencia = None

    # ETAPA 1: COLETA E VALIDAÇÃO
    for arquivo in arquivos_encontrados:
        nome_arq = os.path.basename(arquivo)
        try:
            df_temp = pd.read_csv(arquivo, sep=';', encoding='utf-8')
            colunas_atuais = list(df_temp.columns)

            if colunas_referencia is None:
                colunas_referencia = colunas_atuais
            else:
                if colunas_atuais != colunas_referencia:
                    st.error(f"❌ Arquivo '{nome_arq}' rejeitado por incompatibilidade de colunas.")
                    continue
            
            df_temp['Origem_Arquivo'] = nome_arq
            lista_dfs.append(df_temp)
        except Exception as e:
            st.error(f"❌ Erro ao ler '{nome_arq}': {e}")

    if lista_dfs:
        df_consolidado = pd.concat(lista_dfs, ignore_index=True)

        # ETAPA 2: TRATAMENTO DE DATAS E VALORES
        for col in df_consolidado.columns:
            if any(termo in col.lower() for termo in ['data', 'prazo', 'conclusao', 'inicio', 'fim']):
                def tratar_data_hora(val):
                    if pd.isna(val) or str(val).strip() == '' or str(val).upper() == 'NAN':
                        return None
                    val_str = str(val).strip()
                    dt = pd.to_datetime(val_str, errors='coerce')
                    if pd.isna(dt):
                        return None
                    if ':' in val_str or len(val_str) > 10:
                        return dt.strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        return dt.strftime('%d/%m/%Y') + ' 00:00'
                df_consolidado[col] = df_consolidado[col].apply(tratar_data_hora)

        colunas_monetarias_mapeadas = {}
        for col in df_consolidado.columns:
            if any(termo in col.lower() for termo in ['valor', 'multa', 'preco', 'custo', 'taxa', 'receita', 'faturamento', 'montante']):
                serie_str = df_consolidado[col].astype(str).str.upper()
                serie_limpa = (
                    serie_str.str.replace('R$', '', regex=False)
                    .str.replace('#', '', regex=False)
                    .str.replace('$', '', regex=False)
                    .str.replace('NÃO', '0', regex=False)
                    .str.replace('NAN', '0', regex=False)
                    .str.replace(' ', '', regex=False)
                )
                serie_convertida = []
                for val in serie_limpa:
                    try:
                        val_limpo = val.replace('.', '').replace(',', '.')
                        num = float(val_limpo)
                        serie_convertida.append(round(num, 2))
                    except:
                        serie_convertida.append(0.0)
                df_consolidado[col] = pd.Series(serie_convertida, dtype='float64')
                colunas_monetarias_mapeadas[col] = Numeric(20, 2)

        df_consolidado = df_consolidado.drop_duplicates()

        # ETAPA 3: CARGA NO SUPABASE
        db_user = "postgres"
        db_host = "db.tocehhtqemxhgxuwjykm.supabase.co"
        db_port = "5432"
        db_name = "postgres"

        string_conexao = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

        try:
            engine = create_engine(string_conexao)
            nome_tabela = "tb_compliance_regulatorio_aneel"

            df_consolidado.to_sql(
                name=nome_tabela,
                con=engine,
                if_exists='replace', 
                index=False,
                dtype=colunas_monetarias_mapeadas
            )
            st.success(f"✨ Sucesso! {df_consolidado.shape[0]} linhas enviadas para o Supabase.")
            return True
        except Exception as e:
            st.error(f"❌ Erro ao conectar no Supabase: {e}")
            return False
    else:
        st.error("❌ Nenhum arquivo válido encontrado.")
        return False