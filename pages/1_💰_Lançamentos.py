import streamlit as st
import pandas as pd
from datetime import date
from supabase_utils import insert_data, fetch_data

st.set_page_config(page_title="Lançamentos", page_icon="💰")

st.title("💸 Novo Lançamento")

# Função para buscar categorias sem cache para garantir atualização real
def carregar_categorias():
    try:
        res = fetch_data("categorias")
        if res and res.data:
            return pd.DataFrame(res.data)
    except:
        pass
    return pd.DataFrame(columns=['nome', 'tipo'])

# Carregamos as categorias aqui (fora do form)
df_cat = carregar_categorias()

# Criamos o formulário
with st.form("form_lancamento", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        data_t = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    
    with col2:
        # Quando o usuário mudar aqui, o script vai rodar novamente ao clicar ou interagir
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"], key="tipo_sel")
        
        # Filtra as categorias baseada no tipo selecionado no selectbox acima
        categorias_filtradas = df_cat[df_cat['tipo'] == tipo]['nome'].tolist()
        
        if not categorias_filtradas:
            categorias_filtradas = ["Outros"]
            
        cat = st.selectbox("Categoria", categorias_filtradas)
        metodo = st.selectbox("Método", ["Pix", "Cartão", "Dinheiro", "Boleto"])

    enviar = st.form_submit_button("Salvar Registro")

    if enviar:
        if desc and valor:
            payload = {
                "data_transacao": str(data_t),
                "descricao": desc,
                "valor": valor,
                "tipo": tipo,
                "categoria": cat,
                "metodo_pagamento": metodo
            }
            try:
                insert_data("transacoes", payload)
                st.success(f"Registrado com sucesso: {desc}")
                st.balloons()
                # O rerun limpa o cache visual e recarrega a página
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("Preencha Descrição e Valor.")

# Dica visual para o usuário
if df_cat.empty:
    st.info("💡 Vá em 'Configurações' para cadastrar suas categorias de Receita e Despesa.")
