
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Caminho para o arquivo de dados
DATA_FILE = "bonificacoes.xlsx"

# Função para carregar os dados
def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Data", "Ordem de Serviço", "Bonificação (R$)", "Técnico"])

# Função para salvar os dados
def salvar_dados(df):
    df.to_excel(DATA_FILE, index=False)

# Carregar dados
df = carregar_dados()

# Interface
st.title("Sistema de Bonificações por OS")

# Botão para zerar lançamentos
if st.button("🗑️ Zerar Lançamentos"):
    df = pd.DataFrame(columns=["Data", "Ordem de Serviço", "Bonificação (R$)", "Técnico"])
    salvar_dados(df)
    st.warning("Todos os lançamentos foram apagados.")

# Formulário para novo lançamento
st.subheader("Adicionar Novo Lançamento")
with st.form("form_bonificacao"):
    data = st.date_input("Data do Lançamento")
    os_num = st.text_input("Número da Ordem de Serviço")
    bonificacao = st.number_input("Valor da Bonificação (R$)", min_value=0.0, format="%.2f")
    tecnico = st.text_input("Nome do Técnico")
    submit = st.form_submit_button("Adicionar")

    if submit:
        if os_num.strip() != "" and tecnico.strip() != "":
            data_formatada = datetime.strftime(data, "%d/%m/%Y")
            nova_linha = pd.DataFrame([[data_formatada, os_num.strip(), bonificacao, tecnico.strip()]], columns=df.columns)
            df = pd.concat([df, nova_linha], ignore_index=True)
            salvar_dados(df)
            st.success("Lançamento adicionado com sucesso!")
        else:
            st.error("Todos os campos devem ser preenchidos.")

# Exibir lançamentos
st.subheader("Lançamentos")
st.dataframe(df)

# Resumo
st.subheader("Resumo")
st.metric("Quantidade de Lançamentos", len(df))
st.metric("Total em Bonificações", f"R$ {df['Bonificação (R$)'].sum():.2f}")

# Pódio dos técnicos
st.subheader("🏆 Top 3 Técnicos em Bonificação")

if not df.empty and "Técnico" in df.columns:
    ranking = df.groupby("Técnico")["Bonificação (R$)"].sum().sort_values(ascending=False).reset_index()

    if len(ranking) >= 3:
        col2, col1, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown("🥇 **1º Lugar**")
            st.metric(label=ranking.iloc[0]["Técnico"], value=f"R$ {ranking.iloc[0]['Bonificação (R$)']:.2f}")
        with col2:
            st.markdown("🥈 **2º Lugar**")
            st.metric(label=ranking.iloc[1]["Técnico"], value=f"R$ {ranking.iloc[1]['Bonificação (R$)']:.2f}")
        with col3:
            st.markdown("🥉 **3º Lugar**")
            st.metric(label=ranking.iloc[2]["Técnico"], value=f"R$ {ranking.iloc[2]['Bonificação (R$)']:.2f}")
    else:
        st.info("Ainda não há bonificações suficientes para montar o pódio.")
else:
    st.info("Nenhum dado disponível para exibir o pódio.")
