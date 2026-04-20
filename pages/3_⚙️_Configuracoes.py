import streamlit as st
import pandas as pd
from supabase_utils import insert_data, fetch_data, delete_data

st.set_page_config(page_title="Configurações", page_icon="⚙️")

st.title("⚙️ Configurações do Sistema")

# --- SEÇÃO DE CADASTRO ---
st.subheader("Cadastrar Novas Categorias")
with st.form("novo_cadastro_cat", clear_on_submit=True):
    n_nome = st.text_input("Nome da Categoria")
    n_tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    btn_add = st.form_submit_button("Adicionar Categoria")
    
    if btn_add:
        if n_nome:
            insert_data("categorias", {"nome": n_nome, "tipo": n_tipo})
            st.success(f"Categoria {n_nome} adicionada!")
            st.rerun()

st.divider()

# --- LISTAGEM E EXCLUSÃO ---
st.subheader("Categorias Cadastradas")
res = fetch_data("categorias")

if res and res.data:
    df_c = pd.DataFrame(res.data)
    # Exibe a tabela formatada
    st.dataframe(df_c[['nome', 'tipo']], use_container_width=True)
    
    with st.expander("🗑️ Remover Categoria"):
        escolha = st.selectbox(
            "Selecione para excluir", 
            df_c['id'].tolist(), 
            format_func=lambda x: df_c[df_c['id']==x]['nome'].values[0]
        )
        if st.button("Confirmar Remoção"):
            delete_data("categorias", escolha)
            st.success("Removido com sucesso.")
            st.rerun()
else:
    st.info("Nenhuma categoria encontrada no banco de dados.")
