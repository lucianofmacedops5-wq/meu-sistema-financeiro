import streamlit as st
import pandas as pd
import plotly.express as px
from supabase_utils import fetch_data

st.set_page_config(page_title="Relatórios", layout="wide", page_icon="📊")

st.title("📊 Análise de Gastos")

res = fetch_data("transacoes")

if res and len(res.data) > 0:
    df = pd.DataFrame(res.data)
    df['valor'] = pd.to_numeric(df['valor'])
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Gastos por Categoria")
        fig = px.pie(df[df['tipo'] == 'Despesa'], values='valor', names='categoria', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Receita vs Despesa")
        fig2 = px.bar(df.groupby('tipo')['valor'].sum().reset_index(), x='tipo', y='valor', color='tipo')
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Sem dados para relatórios.")
