import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["url"].strip()
        key = st.secrets["supabase"]["key"].strip()
        if "/rest/v1" in url: url = url.split("/rest/v1")[0]
        url = url.rstrip("/")
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return None

supabase = init_connection()

def fetch_data(table_name):
    if supabase:
        return supabase.table(table_name).select("*").execute()
    return None

def insert_data(table_name, data):
    if supabase:
        return supabase.table(table_name).insert(data).execute()
    return None

def delete_data(table_name, row_id):
    if supabase:
        return supabase.table(table_name).delete().eq("id", row_id).execute()
    return None
