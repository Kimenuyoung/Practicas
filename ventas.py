import sqlite3
import pandas as pd

# Cargar el archivo CSV con datos de ventas de videojuegos
df = pd.read_csv('vgsales.csv')

# Mostrar las primeras 5 filas para inspeccionar estructura y contenido
print(df.head())


# LIMPIEZA DE DATOS

# Eliminar filas duplicadas
df = df.drop_duplicates()

# Reemplazar valores faltantes (NaN) por "Unknown" en columnas categóricas
df = df.fillna("Unknown")

# Convertir Year a numérico (int): valores no convertibles se reemplazan por 0
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)

# ANÁLISIS POR GÉNERO - Ventas globales agrupadas
sales_by_genre = df.groupby("Genre")["Global_Sales"].sum().reset_index()
print("VENTAS GLOBALES POR GÉNERO:")
print(sales_by_genre)

# TOP 5 EDITORES (Publishers) CON MÁS VENTAS GLOBALES
top_publishers = df.groupby("Publisher")[
    "Global_Sales"].sum().nlargest(5).reset_index()
print("TOP 5 EDITORES POR VENTAS GLOBALES:")
print(top_publishers)

# ANÁLISIS DEL MERCADO JAPONÉS (JP_Sales)

# Top 10 juegos más vendidos en Japón
japan_sales = df.groupby("Name")["JP_Sales"].sum().nlargest(10).reset_index()
print("TOP 10 JUEGOS MÁS VENDIDOS EN JAPÓN:")
print(japan_sales)

# Ventas por género en Japón
japan_sales_genre = df.groupby(
    "Genre")["JP_Sales"].sum().nlargest(10).reset_index()
print('\nTOP 10 GÉNEROS MÁS VENDIDOS EN JAPÓN:')
print(japan_sales_genre)

# ANÁLISIS DEL MERCADO DE AMÉRICA DEL NORTE (NA_Sales)

# Top 10 juegos más vendidos en América del Norte
north_america_sales = df.groupby(
    "Name")["NA_Sales"].sum().nlargest(10).reset_index()
print("TOP 10 JUEGOS MÁS VENDIDOS EN AMÉRICA DEL NORTE:")
print(north_america_sales)

# Ventas por género en América del Norte
north_america_sales_genre = df.groupby(
    "Genre")["NA_Sales"].sum().nlargest(10).reset_index()
print('\nTOP 10 GÉNEROS MÁS VENDIDOS EN AMÉRICA DEL NORTE:')
print(north_america_sales_genre)

# ANÁLISIS DEL MERCADO EUROPEO (EU_Sales)

# Top 10 juegos más vendidos en Europa
european_union_sales = df.groupby(
    "Name")["EU_Sales"].sum().nlargest(10).reset_index()
print("TOP 10 JUEGOS MÁS VENDIDOS EN EUROPA:")
print(european_union_sales)

# Ventas por género en Europa
european_union_sales_genre = df.groupby(
    "Genre")["EU_Sales"].sum().nlargest(10).reset_index()
print('\nTOP 10 GÉNEROS MÁS VENDIDOS EN EUROPA:')
print(european_union_sales_genre)


conn = sqlite3.connect("videogames.db")
df.to_sql("vgsales_clean", conn, if_exists="replace", index=False)
sales_by_genre.to_sql("sales_by_genre", conn, if_exists="replace", index=False)
top_publishers.to_sql("top_publishers", conn, if_exists="replace", index=False)
japan_sales.to_sql("japan_sales", conn, if_exists="replace", index=False)
japan_sales_genre.to_sql("jp_genre_sales", conn,
                         if_exists="replace", index=False)
european_union_sales_genre.to_sql(
    "eu_sales", conn, if_exists="replace", index=False)
north_america_sales_genre.to_sql(
    "na_sales", conn, if_exists="replace", index=False)
european_union_sales.to_sql("eu_sales_name", conn,
                            if_exists="replace", index=False)
north_america_sales.to_sql("na_sales_name", conn,
                           if_exists="replace", index=False)

conn.close()

print("Datos cargados en la base de datos.")

try:
    import streamlit as st
except ModuleNotFoundError:
    import sys
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

# Conectar a la base
conn = sqlite3.connect("videogames.db")

# Cargar tabla
df = pd.read_sql("SELECT * FROM vgsales_clean", conn)

# Dashboard
st.title("Ventas de Videojuegos")
st.bar_chart(df.groupby("Genre")["Global_Sales"].sum())
st.line_chart(df.groupby("Year")["Global_Sales"].sum())
