import streamlit as st
import pandas as pd
from datetime import date
from supabase_utils import insert_data, fetch_data

st.set_page_config(page_title="Lançamentos", page_icon="💰")

st.title("💸 Novo Lançamento")

# Tenta carregar categorias
try:
    res_cat = fetch_data("categorias")
    df_cat = pd.DataFrame(res_cat.data)
except:
    df_cat = pd.DataFrame(columns=['nome', 'tipo'])

with st.form("meu_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        data_t = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    with col2:
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
        lista_cat = df_cat[df_cat['tipo'] == tipo]['nome'].tolist() if not df_cat.empty else []
        cat = st.selectbox("Categoria", lista_cat if lista_cat else ["Outros"])
        metodo = st.selectbox("Método", ["Pix", "Cartão", "Dinheiro", "Boleto"])

    if st.form_submit_button("🚀 Gravar no Banco"):
        if desc and valor:
            dados = {
                "data_transacao": str(data_t),
                "descricao": desc,
                "valor": valor,
                "tipo": tipo,
                "categoria": cat,
                "metodo_pagamento": metodo
            }
            try:
                # Tenta salvar
                resultado = insert_data("transacoes", dados)
                st.success(f"✅ Salvo com sucesso: {desc}")
                st.balloons()
            except Exception as e:
                # Se der erro, ele vai mostrar EXATAMENTE o que o Supabase respondeu
                st.error("❌ O Banco de Dados recusou o registro.")
                st.code(f"Erro técnico: {e}")
        else:
            st.warning("Preencha Descrição e Valor.")
