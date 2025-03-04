import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial
st.set_page_config(layout="wide", page_title="Dashboard de Vendas")

# Carregar os dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Barra lateral - Filtros
st.sidebar.header("Filtros")

# Filtro por mês
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtro por cidade (filial)
cities = st.sidebar.multiselect("Filtrar por Filial (Cidade)", df["City"].unique(), default=df["City"].unique())

# Filtro por tipo de produto
product_line = st.sidebar.selectbox("Filtrar por Tipo de Produto", df["Product line"].unique())

# Filtro por intervalo de datas
start_date, end_date = st.sidebar.date_input("Selecione o período", [df["Date"].min(), df["Date"].max()])

# Filtrar os dados
df_filtered = df[(df["Month"] == month) & (df["City"].isin(cities)) & (df["Product line"] == product_line)]
df_filtered = df_filtered[(df_filtered["Date"] >= pd.to_datetime(start_date)) & (df_filtered["Date"] <= pd.to_datetime(end_date))]

# KPIs
st.title("📊 Dashboard de Vendas")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Faturado", f"R$ {df_filtered['Total'].sum():,.2f}")
col2.metric("🛒 Ticket Médio", f"R$ {df_filtered['Total'].mean():,.2f}")
col3.metric("⭐ Avaliação Média", f"{df_filtered['Rating'].mean():.1f}")
col4.metric("🔄 Número de Vendas", f"{df_filtered.shape[0]}")

# Seção de personalização de gráficos na barra lateral
st.sidebar.header("📊 Personalização dos Gráficos")

chart_faturamento = st.sidebar.radio("Faturamento por Dia", ["Barras", "Linha", "Pizza"], key="faturamento")
chart_produto = st.sidebar.radio("Faturamento por Tipo de Produto", ["Barras", "Linha"], key="produto")
chart_filial = st.sidebar.radio("Faturamento por Filial", ["Barras", "Linha"], key="filial")
chart_pagamento = st.sidebar.radio("Faturamento por Tipo de Pagamento", ["Pizza", "Barras"], key="pagamento")
chart_avaliacao = st.sidebar.radio("Avaliação Média por Cidade", ["Barras", "Linha"], key="avaliacao")

# Organizando gráficos em colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico de Faturamento por Dia
if chart_faturamento == "Barras":
    fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por Dia")
elif chart_faturamento == "Linha":
    fig_date = px.line(df_filtered, x="Date", y="Total", color="City", title="Faturamento por Dia")
else:
    fig_date = px.pie(df_filtered, values="Total", names="City", title="Faturamento por Cidade")

col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico de Faturamento por Tipo de Produto
if chart_produto == "Barras":
    fig_prod = px.bar(df_filtered, x="Product line", y="Total", color="City", title="Faturamento por Tipo de Produto")
else:
    fig_prod = px.line(df_filtered, x="Product line", y="Total", color="City", title="Faturamento por Tipo de Produto")

col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico de Faturamento por Filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
if chart_filial == "Barras":
    fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por Filial")
else:
    fig_city = px.line(city_total, x="City", y="Total", title="Faturamento por Filial")

col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico de Faturamento por Tipo de Pagamento
if chart_pagamento == "Pizza":
    fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por Tipo de Pagamento")
else:
    fig_kind = px.bar(df_filtered, x="Payment", y="Total", title="Faturamento por Tipo de Pagamento")

col4.plotly_chart(fig_kind, use_container_width=True)

# Gráfico de Avaliação Média por Cidade
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
if chart_avaliacao == "Barras":
    fig_rating = px.bar(city_rating, x="City", y="Rating", title="Avaliação Média por Cidade")
else:
    fig_rating = px.line(city_rating, x="City", y="Rating", title="Avaliação Média por Cidade")

col5.plotly_chart(fig_rating, use_container_width=True)

# Botão de Download dos Dados Filtrados
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("📥 Baixar Dados", csv, "dados_filtrados.csv", "text/csv")

# Modo Escuro/Claro
theme = st.sidebar.radio("Tema", ["Claro", "Escuro"])
if theme == "Escuro":
    st.markdown("<style>body {background-color: #333; color: white;}</style>", unsafe_allow_html=True)
