import streamlit as st
import pandas as pd
from datetime import date
from supabase_utils import insert_data, fetch_data

st.set_page_config(page_title="Lançamentos", page_icon="💰")

st.title("💸 Novo Lançamento")

# Buscar categorias do banco
res_cat = fetch_data("categorias")
df_cat = pd.DataFrame(res_cat.data) if res_cat and res_cat.data else pd.DataFrame(columns=['nome', 'tipo'])

with st.form("form_financeiro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        data_t = st.date_input("Data", value=date.today())
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    with col2:
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
        # Filtra categorias baseado no tipo
        lista_cat = df_cat[df_cat['tipo'] == tipo]['nome'].tolist()
        cat = st.selectbox("Categoria", lista_cat if lista_cat else ["Outros"])
        metodo = st.selectbox("Método", ["Pix", "Cartão", "Dinheiro", "Boleto"])

    if st.form_submit_button("Salvar"):
        if desc and valor:
            payload = {
                "data_transacao": str(data_t), "descricao": desc, "valor": valor,
                "tipo": tipo, "categoria": cat, "metodo_pagamento": metodo
            }
            insert_data("transacoes", payload)
            st.success("Lançamento salvo!")
            st.rerun()
