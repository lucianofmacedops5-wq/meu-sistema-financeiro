import streamlit as st
import pandas as pd
import plotly.express as px
from supabase_utils import fetch_data

st.set_page_config(page_title="Relatórios", layout="wide", page_icon="📊")

st.title("📊 Análise Financeira Detalhada")

# Busca dados do banco
res = fetch_data("transacoes")

if res and res.data:
    df = pd.DataFrame(res.data)
    df['valor'] = pd.to_numeric(df['valor'])
    df['data_transacao'] = pd.to_datetime(df['data_transacao'])
    df['Mes_Ano'] = df['data_transacao'].dt.strftime('%Y-%m') # Para agrupar mensalmente

    # --- MÉTRICAS GERAIS (Cards) ---
    total_receita = df[df['tipo'] == 'Receita']['valor'].sum()
    total_despesa = df[df['tipo'] == 'Despesa']['valor'].sum()
    saldo_total = total_receita - total_despesa

    m1, m2, m3 = st.columns(3)
    m1.metric("Total de Receitas", f"R$ {total_receita:,.2f}")
    m2.metric("Total de Despesas", f"R$ {total_despesa:,.2f}", delta_color="inverse")
    m3.metric("Saldo Acumulado", f"R$ {saldo_total:,.2f}")

    st.divider()

    # --- LINHA 1 DE GRÁFICOS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Evolução Mensal")
        # Agrupa por mês e tipo para ver a linha do tempo
        df_evolucao = df.groupby(['Mes_Ano', 'tipo'])['valor'].sum().reset_index()
        fig_evolucao = px.line(df_evolucao, x='Mes_Ano', y='valor', color='tipo',
                               title="Receitas vs Despesas por Mês",
                               labels={'Mes_Ano': 'Mês', 'valor': 'Total (R$)'},
                               markers=True, color_discrete_map={'Receita': '#00CC96', 'Despesa': '#EF553B'})
        st.plotly_chart(fig_evolucao, use_container_width=True)

    with col2:
        st.subheader("🍕 Distribuição por Categoria")
        # Filtro para escolher qual tipo ver no gráfico de pizza
        tipo_pizza = st.radio("Ver categorias de:", ["Despesa", "Receita"], horizontal=True)
        df_pizza = df[df['tipo'] == tipo_pizza]
        fig_pizza = px.pie(df_pizza, values='valor', names='categoria', 
                           title=f"Proporção de {tipo_pizza}s",
                           hole=0.4)
        st.plotly_chart(fig_pizza, use_container_width=True)

    st.divider()

    # --- LINHA 2 DE GRÁFICOS ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("💳 Métodos de Pagamento")
        df_metodo = df.groupby('metodo_pagamento')['valor'].count().reset_index()
        df_metodo.columns = ['Método', 'Quantidade']
        fig_metodo = px.bar(df_metodo, x='Método', y='Quantidade', 
                            title="Uso por Meio de Pagamento",
                            color='Método', text_auto=True)
        st.plotly_chart(fig_metodo, use_container_width=True)

    with col4:
        st.subheader("💰 Maiores Gastos (Top 5)")
        # Filtra apenas despesas e pega as maiores
        df_top_gastos = df[df['tipo'] == 'Despesa'].nlargest(5, 'valor')
        fig_top = px.bar(df_top_gastos, x='valor', y='descricao', orientation='h',
                         title="Top 5 Maiores Despesas Individuais",
                         labels={'valor': 'Valor (R$)', 'descricao': 'Item'},
                         color='valor', color_continuous_scale='Reds')
        st.plotly_chart(fig_top, use_container_width=True)

else:
    st.info("Nenhum dado encontrado para gerar relatórios. Comece fazendo alguns lançamentos!")
