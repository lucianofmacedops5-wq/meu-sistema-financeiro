import streamlit as st
import pandas as pd
from datetime import date
from supabase_utils import insert_data, fetch_data

st.set_page_config(page_title="Lançamentos", page_icon="💰")

st.title("💸 Novo Lançamento")

# --- BUSCA CATEGORIAS DO BANCO ---
res_cat = fetch_data("categorias")
if res_cat and res_cat.data:
    df_cat = pd.DataFrame(res_cat.data)
else:
    df_cat = pd.DataFrame(columns=['nome', 'tipo'])

with st.form("form_financeiro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        # Formato de data brasileiro no seletor
        data_t = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    with col2:
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
        
        # Filtragem dinâmica de categorias
        cat_disponiveis = df_cat[df_cat['tipo'] == tipo]['nome'].tolist()
        if not cat_disponiveis:
            cat_disponiveis = ["Outros"]
            
        categoria = st.selectbox("Categoria", cat_disponiveis)
        metodo = st.selectbox("Método", ["Pix", "Cartão", "Dinheiro", "Boleto"])

    if st.form_submit_button("Salvar no Banco"):
        if desc and valor:
            payload = {
                "data_transacao": str(data_t), 
                "descricao": desc, 
                "valor": valor,
                "tipo": tipo, 
                "categoria": categoria, 
                "metodo_pagamento": metodo
            }
            try:
                # Tentativa de inserção com feedback imediato
                resultado = insert_data("transacoes", payload)
                if resultado:
                    st.success(f"Sucesso! {desc} salvo.")
                    st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("Preencha Descrição e Valor.")
