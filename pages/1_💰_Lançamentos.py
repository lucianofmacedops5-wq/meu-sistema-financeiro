import streamlit as st
import pandas as pd
from datetime import date
from supabase_utils import insert_data, fetch_data

st.set_page_config(page_title="Lançamentos", page_icon="💰")

st.title("💸 Novo Lançamento")

# 1. Busca categorias para o seletor
res_cat = fetch_data("categorias")
df_cat = pd.DataFrame(res_cat.data) if res_cat and res_cat.data else pd.DataFrame(columns=['nome', 'tipo'])

with st.form("form_financeiro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        data_t = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
        desc = st.text_input("Descrição (Ex: Compras Mes)")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    with col2:
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
        
        # Filtra categorias baseado no tipo selecionado
        lista_cat = df_cat[df_cat['tipo'] == tipo]['nome'].tolist()
        if not lista_cat:
            st.info("⚠️ Nenhuma categoria deste tipo cadastrada. Usando 'Outros'.")
            lista_cat = ["Outros"]
            
        cat = st.selectbox("Categoria", lista_cat)
        metodo = st.selectbox("Método", ["Pix", "Cartão", "Dinheiro", "Boleto"])

    submit = st.form_submit_button("Confirmar Lançamento")

    if submit:
        if desc and valor:
            # Payload organizado
            payload = {
                "data_transacao": str(data_t),
                "descricao": desc,
                "valor": valor,
                "tipo": tipo,
                "categoria": cat,
                "metodo_pagamento": metodo
            }
            
            try:
                # Tenta inserir
                resultado = insert_data("transacoes", payload)
                if resultado:
                    st.success(f"✅ Sucesso: {desc} registrado!")
                    st.balloons()
            except Exception as e:
                # Mostra o erro real do banco se falhar
                st.error(f"❌ Erro ao salvar no banco: {e}")
        else:
            st.warning("Preencha a Descrição e o Valor.")
