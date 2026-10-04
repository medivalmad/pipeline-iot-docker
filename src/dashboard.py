import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Temperaturas IoT",
    page_icon="🌡️",
    layout="wide",
)


# Conexão com o PostgreSQL
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def carregar_view(nome_view):
    """Carrega os dados de uma view do PostgreSQL."""
    return pd.read_sql(f"SELECT * FROM {nome_view}", engine)


# ============================================================
# Cabeçalho
# ============================================================

st.title("🌡️ Dashboard de Temperaturas IoT")

st.write(
    "Análise das leituras de temperatura coletadas por dispositivos IoT, "
    "processadas com Python e armazenadas em PostgreSQL."
)


# ============================================================
# Indicadores principais
# ============================================================

df_resumo = pd.read_sql(
    """
    SELECT
        COUNT(*) AS total_leituras,
        ROUND(AVG(temp)::numeric, 2) AS temperatura_media,
        MIN(temp) AS temperatura_minima,
        MAX(temp) AS temperatura_maxima
    FROM temperature_readings
    """,
    engine,
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total de leituras",
    f"{int(df_resumo['total_leituras'].iloc[0]):,}".replace(",", "."),
)

col2.metric(
    "Temperatura média",
    f"{float(df_resumo['temperatura_media'].iloc[0]):.2f} °C",
)

col3.metric(
    "Temperatura mínima",
    f"{int(df_resumo['temperatura_minima'].iloc[0])} °C",
)

col4.metric(
    "Temperatura máxima",
    f"{int(df_resumo['temperatura_maxima'].iloc[0])} °C",
)


# ============================================================
# Gráfico 1
# ============================================================

st.header("Temperatura Média por Ambiente")

df_ambiente = carregar_view("avg_temp_por_ambiente")

fig1 = px.bar(
    df_ambiente,
    x="ambiente",
    y="avg_temp",
    text="avg_temp",
    labels={
        "ambiente": "Ambiente",
        "avg_temp": "Temperatura média (°C)",
    },
)

fig1.update_traces(texttemplate="%{text:.2f} °C", textposition="outside")

st.plotly_chart(fig1, use_container_width=True)


# ============================================================
# Gráfico 2
# ============================================================

st.header("Quantidade de Leituras por Hora")

df_hora = carregar_view("leituras_por_hora")

fig2 = px.line(
    df_hora,
    x="hora",
    y="contagem",
    markers=True,
    labels={
        "hora": "Hora do dia",
        "contagem": "Quantidade de leituras",
    },
)

st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# Gráfico 3
# ============================================================

st.header("Variação de Temperatura por Dia")

df_dia = carregar_view("temp_por_dia")

fig3 = px.line(
    df_dia,
    x="data",
    y=["temp_min", "temp_media", "temp_max"],
    labels={
        "data": "Data",
        "value": "Temperatura (°C)",
        "variable": "Métrica",
    },
)

st.plotly_chart(fig3, use_container_width=True)