import streamlit as st
from supabase import create_client

@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["url"].strip().rstrip("/")
        key = st.secrets["supabase"]["key"].strip()
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

supabase = init_connection()

def fetch_data(table_name):
    return supabase.table(table_name).select("*").execute()

def insert_data(table_name, data):
    # Esta versão captura o erro específico do banco
    response = supabase.table(table_name).insert(data).execute()
    return response

def delete_data(table_name, row_id):
    return supabase.table(table_name).delete().eq("id", row_id).execute()
