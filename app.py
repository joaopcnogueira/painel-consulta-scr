import pandas as pd
import streamlit as st
from neoscr.core import ConsultaSCR
from neoscr.utils import let_only_digits
from pathlib import Path

from src.dates import get_current_data_base
from src.download import download_button


st.title("Painel de Consulta SCR - CresceAI")

@st.cache_resource
def get_cpf_data(cpf, ano, mes):
    df_cpf_traduzido, df_cpf_modalidade, df_cpf_resumo_lista_das_operacoes = neoscr.get_cpf_data(cpf, ano, mes)
    return df_cpf_traduzido, df_cpf_modalidade, df_cpf_resumo_lista_das_operacoes

@st.cache_resource
def get_cnpj_data(cnpj, ano, mes):
    df_cnpj_traduzido, df_cnpj_modalidade, df_cnpj_resumo_lista_das_operacoes = neoscr.get_cnpj_data(cnpj, ano, mes)
    return df_cnpj_traduzido, df_cnpj_modalidade, df_cnpj_resumo_lista_das_operacoes


with st.form("Painel de Consulta"):
    st.subheader("Consulta Simples")
    cnpj = st.text_input('Digite o CNPJ', placeholder='00.000.000/0000-00')
    cpf = st.text_input('Digite o CPF', placeholder='000.000.000-00')
    data_base = st.text_input('Data Base', placeholder='MM/AAAA', value=get_current_data_base())
    submitted = st.form_submit_button("Consultar")


if submitted:
    mes, ano = int(data_base.split("/")[0]), int(data_base.split("/")[1])

    neoscr = ConsultaSCR() # Need to have the env variables set. For reference, see the neoscr documentation
    
    try:
        df_cpf_traduzido, df_cpf_modalidade, df_cpf_resumo_lista_das_operacoes = get_cpf_data(cpf, ano, mes)
        df_cnpj_traduzido, df_cnpj_modalidade, df_cnpj_resumo_lista_das_operacoes = get_cnpj_data(cnpj, ano, mes)

        st.success("Consulta realizada com sucesso!")
        st.info("Caso não apareça uma tabela, significa que não há dados para o CNPJ/CPF consultado na data base informada.")

        st.header("Dados do CPF")
        st.caption("Tabela com informações traduzidas")        
        st.dataframe(df_cpf_traduzido)

        st.caption("Tabela com sobre as modalidades")        
        st.dataframe(df_cpf_modalidade)

        st.caption("Tabela com informações sobre as modalidades no tempo")        
        st.dataframe(df_cpf_resumo_lista_das_operacoes)

        st.header("Dados do CNPJ")
        st.caption("Tabela com informações resumidas")        
        st.dataframe(df_cnpj_traduzido)

        st.caption("Tabela com sobre as modalidades")        
        st.dataframe(df_cnpj_modalidade)

        st.caption("Tabela com informações sobre as modalidades no tempo")        
        st.dataframe(df_cnpj_resumo_lista_das_operacoes)

    except Exception as e:
        st.error("Erro ao consultar dados: {}".format(e))
