import streamlit as st
import pandas as pd
from supabase_utils import fetch_data, delete_data

st.set_page_config(page_title="Finanças Pro", layout="wide", page_icon="📈")

st.title("🚀 Dashboard Financeiro")

res = fetch_data("transacoes")

if res and len(res.data) > 0:
    df = pd.DataFrame(res.data)
    df['valor'] = pd.to_numeric(df['valor'])
    df['data_transacao'] = pd.to_datetime(df['data_transacao'])
    
    # Filtros
    st.sidebar.header("Filtros")
    df['Mes'] = df['data_transacao'].dt.month
    df['Ano'] = df['data_transacao'].dt.year
    
    ano_sel = st.sidebar.selectbox("Ano", sorted(df['Ano'].unique(), reverse=True))
    mes_sel = st.sidebar.selectbox("Mês", range(1, 13), format_func=lambda x: ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"][x-1])
    
    df_f = df[(df['Ano'] == ano_sel) & (df['Mes'] == mes_sel)]

    c1, c2, c3 = st.columns(3)
    rec = df_f[df_f['tipo'] == 'Receita']['valor'].sum()
    des = df_f[df_f['tipo'] == 'Despesa']['valor'].sum()
    
    c1.metric("Receitas", f"R$ {rec:,.2f}")
    c2.metric("Despesas", f"R$ {des:,.2f}", delta_color="inverse")
    c3.metric("Saldo", f"R$ {rec - des:,.2f}")

    st.divider()
    st.subheader("📋 Lançamentos do Mês")
    if not df_f.empty:
        st.dataframe(df_f.sort_values('data_transacao', ascending=False), use_container_width=True)
        
        with st.expander("🗑️ Excluir Lançamento"):
            id_del = st.selectbox("ID para remover", df_f['id'].tolist())
            if st.button("Remover"):
                delete_data("transacoes", id_del)
                st.rerun()
    else:
        st.info("Sem dados para este mês.")
else:
    st.info("Nenhum registro encontrado.")
