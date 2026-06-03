import pandas as pd
import sqlite3

try:
    import streamlit as st
except ModuleNotFoundError:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

# ==========================================
# Cargar dataset
# ==========================================
df = pd.read_csv("vgsales.csv")

# ==========================================
# Limpieza de datoscls
# ==========================================
df = df.drop_duplicates()
df = df.fillna("Unknown")

df["Year"] = pd.to_numeric(
    df["Year"],
    errors="coerce"
).fillna(0).astype(int)

# ==========================================
# TABLA 1 - Ventas globales por género
# ==========================================
sales_by_genre = (
    df.groupby("Genre")["Global_Sales"]
    .sum()
    .reset_index()
)

# ==========================================
# TABLA 2 - Top 5 publishers
# ==========================================
top_publishers = (
    df.groupby("Publisher")["Global_Sales"]
    .sum()
    .nlargest(5)
    .reset_index()
)

# ==========================================
# TABLA 3 - Ventas en Japón por videojuego
# ==========================================
japan_sales = (
    df.groupby("Name")["JP_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="JP_Sales", ascending=False)
)

# ==========================================
# TABLA 4 - Ventas en Japón por género
# ==========================================
jp_genre_sales = (
    df.groupby("Genre")["JP_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="JP_Sales", ascending=False)
)

# ==========================================
# TABLA 5 - Ventas en Europa por género
# ==========================================
eu_sales = (
    df.groupby("Genre")["EU_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="EU_Sales", ascending=False)
)

# ==========================================
# TABLA 6 - Ventas en Norteamérica por género
# ==========================================
na_sales = (
    df.groupby("Genre")["NA_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="NA_Sales", ascending=False)
)

# ==========================================
# TABLA 7 - Ventas en Europa por videojuego
# ==========================================
eu_sales_name = (
    df.groupby("Name")["EU_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="EU_Sales", ascending=False)
)

# ==========================================
# TABLA 8 - Ventas en Norteamérica por videojuego
# ==========================================
na_sales_name = (
    df.groupby("Name")["NA_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="NA_Sales", ascending=False)
)

# ==========================================
# TABLA 9 - Ventas en Otras Regiones
# ==========================================
other_sales = (
    df.groupby("Genre")["Other_Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Other_Sales", ascending=False)
)

# ==========================================
# Guardar en SQLite
# ==========================================
conn = sqlite3.connect("videogames.db")

df.to_sql("vgsales_clean", conn, if_exists="replace", index=False)
sales_by_genre.to_sql("sales_by_genre", conn, if_exists="replace", index=False)
top_publishers.to_sql("top_publishers", conn, if_exists="replace", index=False)
japan_sales.to_sql("japan_sales", conn, if_exists="replace", index=False)
jp_genre_sales.to_sql("jp_genre_sales", conn, if_exists="replace", index=False)
eu_sales.to_sql("eu_sales", conn, if_exists="replace", index=False)
na_sales.to_sql("na_sales", conn, if_exists="replace", index=False)
eu_sales_name.to_sql("eu_sales_name", conn, if_exists="replace", index=False)
na_sales_name.to_sql("na_sales_name", conn, if_exists="replace", index=False)
other_sales.to_sql("other_sales", conn, if_exists="replace", index=False)

print("Datos cargados en la base de datos.")

# ==========================================
# Dashboard Streamlit
# ==========================================

st.title("🎮 Dashboard de Ventas de Videojuegos")

st.subheader("Datos limpios")
st.dataframe(df.head(20))

st.subheader("Ventas Globales por Género")
st.bar_chart(
    df.groupby("Genre")["Global_Sales"].sum()
)

st.subheader("Ventas Globales por Año")
st.line_chart(
    df.groupby("Year")["Global_Sales"].sum()
)

st.subheader("Ventas por Género en Norteamérica")
st.bar_chart(
    df.groupby("Genre")["NA_Sales"].sum()
)

st.subheader("Ventas por Género en Europa")
st.bar_chart(
    df.groupby("Genre")["EU_Sales"].sum()
)

st.subheader("Ventas por Género en Japón")
st.bar_chart(
    df.groupby("Genre")["JP_Sales"].sum()
)

st.subheader("Ventas por Género en Otras Regiones")
st.bar_chart(
    df.groupby("Genre")["Other_Sales"].sum()
)

st.subheader("Top 5 Publishers")
st.dataframe(top_publishers)

st.subheader("Top Juegos en Japón")
st.dataframe(japan_sales.head(10))

conn.close()