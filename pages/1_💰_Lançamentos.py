import streamlit as st
import pandas as pd
from datetime import date
from supabase_utils import insert_data, fetch_data

st.set_page_config(page_title="Lançamentos", page_icon="💰")

st.title("💸 Novo Lançamento")

# Função para buscar categorias
def carregar_categorias():
    try:
        res = fetch_data("categorias")
        if res and res.data:
            return pd.DataFrame(res.data)
    except:
        pass
    return pd.DataFrame(columns=['nome', 'tipo'])

df_cat = carregar_categorias()

# --- CAMPO FORA DO FORMULÁRIO PARA ATUALIZAÇÃO EM TEMPO REAL ---
# Colocamos o Tipo fora do form para que a categoria mude assim que você clicar
tipo = st.selectbox("Tipo", ["Despesa", "Receita"], key="tipo_principal")

# Filtra as categorias baseada no tipo selecionado acima
categorias_filtradas = df_cat[df_cat['tipo'] == tipo]['nome'].tolist()
if not categorias_filtradas:
    categorias_filtradas = ["Outros"]

# --- INÍCIO DO FORMULÁRIO ---
with st.form("form_lancamento", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        data_t = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    
    with col2:
        # A categoria agora usa a lista filtrada em tempo real
        cat = st.selectbox("Categoria", categorias_filtradas)
        metodo = st.selectbox("Método", ["Pix", "Cartão", "Dinheiro", "Boleto"])

    enviar = st.form_submit_button("Salvar Registro")

    if enviar:
        if desc and valor:
            payload = {
                "data_transacao": str(data_t),
                "descricao": desc,
                "valor": valor,
                "tipo": tipo, # Pega o valor do seletor que está fora do form
                "categoria": cat,
                "metodo_pagamento": metodo
            }
            try:
                insert_data("transacoes", payload)
                st.success(f"✅ Registrado com sucesso: {desc}")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("Preencha Descrição e Valor.")

if df_cat.empty:
    st.info("💡 Nenhuma categoria encontrada. Cadastre em 'Configuracoes'.")
