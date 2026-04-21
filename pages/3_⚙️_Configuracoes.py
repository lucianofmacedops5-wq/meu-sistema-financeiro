import streamlit as st
import pandas as pd
from supabase_utils import insert_data, fetch_data, delete_data

st.set_page_config(page_title="Configurações", page_icon="⚙️")

st.title("⚙️ Gerenciar Categorias")

st.markdown("""
Cadastre aqui os tipos de despesas e receitas que você utiliza. 
*Ex: Aluguel (Despesa), Salário (Receita).*
""")

with st.form("add_cat", clear_on_submit=True):
    n_nome = st.text_input("Nome da Categoria")
    n_tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    if st.form_submit_button("Salvar Categoria"):
        if n_nome:
            insert_data("categorias", {"nome": n_nome, "tipo": n_tipo})
            st.success("Categoria adicionada!")
            st.rerun()

st.divider()

st.subheader("📋 Suas Categorias")
res = fetch_data("categorias")
if res and res.data:
    df_c = pd.DataFrame(res.data)
    st.table(df_c[['nome', 'tipo']])
    
    with st.expander("🗑️ Remover Categoria"):
        id_del = st.selectbox("ID", df_c['id'].tolist(), format_func=lambda x: df_c[df_c['id']==x]['nome'].values[0])
        if st.button("Remover"):
            delete_data("categorias", id_del)
            st.rerun()
